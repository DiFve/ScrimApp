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
            team = {
                'teamName': body['teamName'][0],
                'teamRank': body['teamRank'][0],
                'teamRating': body['teamRating'][0],
                'teamLead' : body['teamLead'][0],
                'teamPost' : [],
                'teamMember' : [],
                'bio' : 'show experiance of your team skill WOOOOOHOOOOO',
            }
            result=db.Test.Team.insert_one(
                {'teamData': team,
                },
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
            db.Test.Team.update_one(
                {'_id':ObjectId(pk)},
                {'$push':{'teamMember':member}}
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

    


            

