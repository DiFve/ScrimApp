from time import time
from django.http import JsonResponse,QueryDict
from django.http.response import HttpResponse
from django.http.request import HttpRequest
import requests
from utils import get_db_handle
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
from .algorithm import postAlgo
import json
import requests

db=get_db_handle()

#don't forget to remove below code when deploy
@csrf_exempt
def createPost(request):
    res={}
    message=''
    statusCode = 200
    if request.method == 'POST':
        try:
            body=dict(request.POST)
            post = {
                'time': body['time'][0],
                'date': body['date'][0],
                'teamRank': 'NoRank',
                'createdby': body['createdby'][0],
                'opponent': '',
                'teamName':body['teamName'][0],
                'isReady':False,
            }
            resformBack = requests.get('http://34.124.169.53:8000/api/getteam/{0}'.format(post['createdby']))
            teamMember=resformBack.json()['reqTeam']['teamMember']
            print(teamMember)
            post['teamRank']=postAlgo.findAvgRank(teamMember)
            if post['teamRank']== None:
                post['teamRank']='No Informations'
            result=db.Test.Post.insert_one(
                {'postData': post,
                'req':[],
                'paticipants': teamMember,
                },
            )
            db.Test.Team.update_one(
                {'_id':ObjectId(post['createdby'])},
                {'$push':{'teamData.teamPost':str(result.inserted_id)}}
            )
            print('lol')
            message='successfully save'
        except Exception as err:
            statusCode = 440
            message='something went wrong saving: ' + str(err.args[0])
    else:
        statusCode = 440
        message='wrong method try again'
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    return JsonResponse(res)
               
def getAllPost(request):
    res={}
    message=''
    statusCode = 200
    allpostLis=[]
    try:
        if request.method == 'GET':
            allpost=db.Test.Post.find()
            postAlgo.updatePassDatePost(db)
            allpostLis=[]
            for data in allpost:
                print(data)
                team = db.Test.Team.find(
                    {'_id': ObjectId(data['postData']['createdby'])}
                )
                if team == None:
                    raise Exception('This team is not exist')
                db.Test.Post.update(
                    {'_id': data['_id']},
                    {
                        '$set':
                        {
                            'postData.teamRank' : postAlgo.findAvgRank(team[0]['teamMember'])
                        }
                    }
                )
            allpost=db.Test.Post.find()
            for data in allpost:
                _id=str(data['_id'])
                data['postData'].update({'id':_id})
                data['postData'].update({'req':data['req']})
                allpostLis.append(data['postData'])
                
            message='successfully finding'
    except Exception as err:
            statusCode = 440
            message='something went wrong finding: ' + str(err.args[0])
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    res.update({'allPosts': allpostLis})
    return JsonResponse(res)

@csrf_exempt
def reqToScrim(request,pk):
        res={}
        message=''
        statusCode = 200
        try:
            body=dict(QueryDict(request.body))
            if request.method == "PUT":
                reqPost = db.Test.Post.find_one(
                {'_id': ObjectId(pk)},
                )
                print(reqPost)
                if body['teamId'][0] == reqPost['postData']['createdby']:
                    raise Exception('Cannot request to your own post')
                if body['teamId'][0] == '':
                    raise Exception('Cannot request with no team')
                for req in list(reqPost['req']):
                    if req['teamId']==body['teamId'][0]:
                        raise Exception('you already requested this post')
                reqToSent = {
                    'teamId': body['teamId'][0],
                }
                db.Test.Post.update_one(
                    {'_id':ObjectId(pk)},
                    {
                        '$push':{'req': reqToSent}
                    }
                )
                message='successfully add your request'
        except Exception as err:
            message='something went wrong while adding your request : ' + str(err.args[0])
        res.update({'statusCode':statusCode})
        res.update({'message':message})
        return JsonResponse(res)

@csrf_exempt
def acceptReq(request,pk):
    res={}
    message=''
    statusCode = 200
    try:
        if request.method == "PUT":
            postId=pk
            body=dict(QueryDict(request.body))
            print(body)
            teamId = body['teamId'][0]
            team=db.Test.Team.find_one(
                {'_id':ObjectId(teamId)}
            )
            
            print(team)
            post=db.Test.Post.find_one(
                {'_id':ObjectId(pk)}
            )
            db.Test.Post.update(
                {'_id':ObjectId(postId)},
                {
                    '$set':
                    {
                        'postData.opponent':teamId,
                        'req':[],
                        'postData.isReady':True
                    }
                }
            )
            for member in team['teamMember']:
                db.Test.Post.update(
                    {'_id' : ObjectId(postId)},
                    {
                        '$push':{'paticipants':{'userId':member['userid']}}
                    }
                )
                db.Test.User.update_one(
                    {'_id' : ObjectId(member['userid'])},
                    {'$push':{'match':postId}}
                )
            print(post)
            postTeam = db.Test.Team.find_one(
                {'_id':ObjectId(post['postData']['createdby'])}
            )
            for member in postTeam['teamMember']:
                db.Test.User.update_one(
                    {'_id':ObjectId(member['userid'])},
                    {'$push':{'match':postId}}
                )
            
            message = 'successfully accept your request'
    except Exception as err:
        message='something went wrong while accepting your request : ' + str(err.args[0])
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    return JsonResponse(res)

@csrf_exempt
def rejectReq(request,pk):
    res={}
    message='OK'
    statusCode = 200
    try:
        if request.method == "PUT":
            postId=pk
            body=dict(QueryDict(request.body))
            teamId = body['teamId'][0]
            post = db.Test.Post.update(
                {'_id':ObjectId(postId)},
                {
                    '$pull':
                    {
                        'req':{
                            'teamId' : teamId
                        }
                    }
                }
            )
            print(post)
    except Exception as err:
         message='something went wrong while rejecting your request : ' + str(err.args[0])
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    return JsonResponse(res)

def getPostById(request,pk):
    res={}
    message=''
    statusCode = 200
    try:
        if request.method == 'GET':
            reqPost = db.Test.Post.find_one(
                {'_id':ObjectId(pk)},
                )
            if reqPost == None:
                raise Exception('No post of that Id found')
            reqPost['_id']=str(reqPost['_id'])
            print(reqPost)
    except Exception as err:
        statusCode = 500
        message = 'something went wrong finding the post : ' + str(err.args[0])
    res.update({'statusCode' : statusCode,
                'message' : message,
                'reqPost' : reqPost
                })
    return JsonResponse(res)

def getPostSort(request):
    res={}
    message=''
    statusCode = 200
    allpost={}
    sortedLis=[]
    try:
        if request.method == 'GET':
            body = dict(QueryDict(request.body))
            allpost=db.Test.Post.find()
            allpostLis=[]
            for data in allpost:
                _id=str(data['_id'])
                data['postData'].update({'id':_id})
                data['postData'].update({'req':data['req']})
                allpostLis.append(data['postData'])
            sortedLis=postAlgo.sortPostBy(body['method'][0],{'allPosts':allpostLis})
            message='successfully finding'
    except Exception as err:
            statusCode = 440
            message='something went wrong finding: ' + str(err.args[0])
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    res.update({'allPosts': sortedLis})
    return JsonResponse(res)

def getAvgRank(request,pk):
    resformBack = requests.get('http://34.124.169.53:8000/api/getteam/{0}'.format(pk))
    teamMember=resformBack.json()['reqTeam']['teamMember']
    rank=postAlgo.findAvgRank(teamMember)
    return JsonResponse({'rank':rank})

def getAllUserPost(request,pk):
    res={}
    message=''
    statusCode = 200
    allpostLis=[]
    print('hello')
    try:
        if request.method == 'GET':
            user=db.Test.User.find_one(
                {'_id':ObjectId(pk)}
            )
            
            allPostId=dict(user)['match']
            print(allPostId)
            allpostLis=[]
            for postId in allPostId:
                post=requests.get('http://34.124.169.53:8000/api/getpost/{0}'.format(postId))
                allpostLis.append(post.json()['reqPost'])
            message='successfully finding'
    except Exception as err:
            statusCode = 440
            message='something went wrong finding: ' + str(err.args[0])
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    res.update({'allUserMatches': allpostLis})
    return JsonResponse(res)