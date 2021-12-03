from time import time
from django.http import JsonResponse,QueryDict
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from utils import get_db_handle
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
import json

db=get_db_handle()

@csrf_exempt
def createTeam(request):
    res={}
    message=''
    statusCode = 200
    if request.method == 'POST':
        try:
            body=dict(request.POST)
            check = db.Test.Team.find(
                {'teamName' : body['teamName'][0]}
            )
            if check != None:
                raise Exception('teamName already exists')
            team = {
                'teamName': body['teamName'][0], #name input
                'teamRank': body['teamRank'][0], #rank of user who created the post
                'teamLead' : body['teamLead'][0], #id of user who created the post
                'teamPost' : [],
                'bio' : 'show experiance of your team skill WOOOOOHOOOOO',
            }
            result=db.Test.Team.insert_one(
                {'teamData': team,
                },
            )
            db.Test.User.update_one(
                {'_id':ObjectId(body['teamLead'][0])},
                {'$set':{'user.team':str(result.inserted_id)}}
            )
            message='successfully save'
        except Exception as err:
            statusCode = 440
            message='something went wrong saving: ' + err.args[0]
    else:
        statusCode = 440
        message='wrong method try again'
    res.update({'statusCode':statusCode,})
    res.update({'message':message})
    return JsonResponse(res)
               
def getTeam(request,pk):
    res={}
    message=''
    statusCode = 200
    if request.method == 'GET':
        try:
            reqTeam = db.Test.Team.find_one(
                {'_id':ObjectId(pk)},
            )
            if reqTeam == None:
                raise Exception('No post of that Id found')

            reqTeam['_id']=str(reqTeam['_id'])
        except Exception as err:
            statusCode = 440
            message='something went wrong saving: ' + err.args[0]
    else:
        statusCode = 440
        message='wrong method try again'
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    res.update({'reqTeam':reqTeam})
    return JsonResponse(res)

@csrf_exempt
def addMember(request,pk):
    res = {}
    message=''
    statusCode = 200

    body=dict(QueryDict(request.body))
    if request.method == 'PUT':
        try:
            member = {
                'userid':body['userid'][0],
                }
            team=db.Test.Team.find_one(
                {'_id':ObjectId(pk)},
            )
            nowMember=[]
            for memberi in team['teamMember']:
                nowMember.append(memberi.get('userid'))
            if body['userid'][0] in nowMember:
                raise Exception('user already in the team')
            
            result=db.Test.Team.update_one(
                {'_id':ObjectId(pk)},
                {'$push':{'teamMember':member}}
            )
            db.Test.User.update_one(
                {'_id':ObjectId(body['userid'][0])},
                {'$set':{'user.team':pk}}
            )
            message='succesfully add your member'
        except Exception as err:
            statusCode = 440
            message='something went wrong saving: ' + err.args[0]
    res.update({
        'statusCode':statusCode,
        'message':message,
        })
    return JsonResponse(res)

@csrf_exempt
def removeMember(request,pk):
    res = {}
    message=''
    statusCode = 200

    body=dict(QueryDict(request.body))
    if request.method == 'PUT':
        try:
            member = {
                'userid':body['userid'][0],
                }
            db.Test.Team.update_one(
                {'_id':ObjectId(pk)},
                {'$pull':{'teamMember':member}}
            )
            message = 'succesfully remove your member'
        except Exception as err:
            statusCode = 440
            message='something went wrong saving: ' + err.args[0]
    res.update({
        'statusCode':statusCode,
        'message':message,
        })
    return JsonResponse(res)

    


            

