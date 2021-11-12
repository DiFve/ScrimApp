from time import time
from django.http import JsonResponse,QueryDict
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from utils import get_db_handle
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
import json

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
                'teamRank': body['teamRank'][0],
                'teamRating' : float(body['teamRating'][0]),
                'details' : 'It\'s a one two three test',
            }
            result=db.Test.Post.insert_one(
                {'postData': post,
                'req':[],
                },
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
