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
            for member in teamMember:
                db.Test.User.update_one(
                    {'_id':ObjectId(member['userid'])},
                    {'$push':{'match':str(result.inserted_id)}}
                )
            db.Test.Team.update_one(
                {'_id':ObjectId(post['createdby'])},
                {'$push':{'teamData.teamPost':str(result.inserted_id)}}
            )
            print('lol')
            message='successfully save'
        except Exception as err:
            statusCode = 440
            message='something went wrong saving: ' + err.args[0]
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
    try:
        if request.method == 'GET':
            allpost=db.Test.Post.find()
            allpostLis=[]
            for data in allpost:
                _id=str(data['_id'])
                data['postData'].update({'id':_id})
                allpostLis.append(data['postData'])
            message='successfully finding'
    except Exception as err:
            statusCode = 440
            message='something went wrong finding: ' + err.args[0]
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
                print(body)
                print(pk)
                reqPost = db.Test.Post.find(
                {'_id': ObjectId(pk)},
                )
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
            message='something went wrong while adding your request : ' + err.args[0]
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
            message = 'successfully accept your request'
    except Exception as err:
        message='something went wrong while accepting your request : ' + err.args[0]
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
        message = 'something went wrong finding the post : ' + err.args[0]
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
                allpostLis.append(data['postData'])
            sortedLis=postAlgo.sortPostBy(body['method'][0],{'allPosts':allpostLis})
            message='successfully finding'
    except Exception as err:
            statusCode = 440
            message='something went wrong finding: ' + err.args[0]
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    res.update({'allPosts': sortedLis})
    return JsonResponse(res)

def getAvgRank(request,pk):
    resformBack = requests.get('http://34.124.169.53:8000/api/getteam/{0}'.format(pk))
    teamMember=resformBack.json()['reqTeam']['teamMember']
    rank=postAlgo.findAvgRank(teamMember)
    return JsonResponse({'rank':rank})

def getAllTeamPost(request,pk):
    res={}
    message=''
    statusCode = 200
    allpostLis=[]
    print('hello')
    try:
        if request.method == 'GET':
            team=db.Test.Team.find_one(
                {'_id':ObjectId(pk)}
            )
            
            allPostId=dict(team)['teamData']['teamPost']
            print(allPostId)
            allpostLis=[]
            for postId in allPostId:
                post=requests.get('http://34.124.169.53:8000/api/getpost/{0}'.format(postId))
                allpostLis.append(post.json()['reqPost'])
            message='successfully finding'
    except Exception as err:
            statusCode = 440
            message='something went wrong finding: ' + err.args[0]
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    res.update({'allTeamPosts': allpostLis})
    return JsonResponse(res)