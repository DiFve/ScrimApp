from time import time
from django.http import JsonResponse,QueryDict
from django.http.response import HttpResponse
from django.http.request import HttpRequest
import requests
from utils import get_db_handle
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
import json
from .algorithm import postAlgo

db=get_db_handle()

@csrf_exempt
def createTeam(request):
    res={}
    message=''
    statusCode = 200
    if request.method == 'POST':
        try:
            body=dict(request.POST)
            if body['teamName'][0] == '':
                raise Exception('teamName cannot be blank')
            check = db.Test.Team.find_one(
                {'teamData.teamName' : body['teamName'][0]}
            )
            checkifhaveteam = db.Test.User.find(
                {'_id':ObjectId(body['teamLead'][0])}
            )
            if checkifhaveteam == None:
                raise Exception('user invalid')
            if checkifhaveteam[0]['user']['team'] != '':
                raise Exception('User alreay have a team')
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
                 'teamMember':[{'userid':body['teamLead'][0]}],
                 'teamMatch':[],
                },
            )
            print(result)
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
    message='OK'
    statusCode = 200
    if request.method == 'GET':
        try:
            reqTeam = db.Test.Team.find_one(
                {'_id':ObjectId(pk)},
            )
            if reqTeam == None:
                raise Exception('No post of that Id found')

            updateRank=db.Test.Team.update(
                {'_id':ObjectId(pk)},
                {
                    '$set':
                    {
                        'teamData.teamRank':postAlgo.findAvgRank(reqTeam['teamMember'])
                    }
                }
            )
            reqTeam = db.Test.Team.find_one(
                {'_id':ObjectId(pk)},
            )
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
            checkifhaveteam = db.Test.User.find(
                {'_id':ObjectId(body['userid'][0])}
            )
            if checkifhaveteam == None:
                raise Exception('User not exist')
            if checkifhaveteam[0]['user']['team'] != '':
                raise Exception('User alreay have a team')
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

    if request.method == 'PUT':
        try:
            body=dict(QueryDict(request.body))
            member = {
                'userid':body['userid'][0],
                }
            user = db.Test.User.update_one(
                {'_id':ObjectId(body['userid'][0])},
                {'$set':{'user.team':'','match':[]}}
            )

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

@csrf_exempt
def editTeam(request,pk):
    res={}
    message = ''
    statusCode = 200

    if request.method == 'PUT':
        try:
            body = dict(QueryDict(request.body))
            check = db.Test.Team.find(
                {'_id':ObjectId(pk)}
            )
            if check == None:
                raise Exception('team not exist')
            team = db.Test.Team.update(
                {'_id':ObjectId(pk)},
                {'$set':
                    {
                        'teamData.teamName':body['teamName'][0],
                        'teamData.bio':body['bio'][0]
                    }
                }
            )
        except Exception as err:
            statusCode = 440
            message='something went wrong saving: ' + err.args[0]
    message = 'OK'
    res.update({
        'statusCode':statusCode,
        'message':message,
        })
    return JsonResponse(res)

            

