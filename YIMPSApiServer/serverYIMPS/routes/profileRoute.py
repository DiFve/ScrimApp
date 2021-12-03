from django.http import JsonResponse,QueryDict
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from dns.rdatatype import NINFO
from utils import get_db_handle
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
import json
import bcrypt

db=get_db_handle()

@csrf_exempt
def creteProfile(request):
    res={}
    message=''
    statusCode = 200
    if request.method == 'POST':
        try:
            body=dict(request.POST)
            salt = bcrypt.gensalt()

            if body['username'][0] == '':
                raise Exception('Please fill your username')
            
            if body['password'][0] == '':
                raise Exception('Please fill your password')
            username = body['username'][0]
            password = str(body['password'][0]).encode("utf-8")


            isUsernameExist = db.Test.User.find_one(
                {'user.username':username}
            )

            print(isUsernameExist)
            if isUsernameExist != None:
                raise Exception('This username is already exist')

            

            hashed = bcrypt.hashpw(password,salt)

            user = {
                'username': username,
                'password': hashed,
                'bio':'',
                'rank':'',
                'team':'',
            }  

            db.Test.User.insert_one(
                {
                    'user': user,
                    'match':[]
                }
            )
            message = 'successfully'

        except Exception as err:
            statusCode = 440
            message='something went wrong : ' + err.args[0]
    else:
        statusCode = 440
        message = 'wrong method try again'
    res.update({'statusCode':statusCode})
    res.update({'message':message})
    return JsonResponse(res)

def login(request):
    res={}
    message=''
    statusCode = 200
    req = ''
    teamID = ''
    try:
        if request.method == 'GET':
            body = dict(QueryDict(request.body))
            username = body['username'][0]
            password = str(body['password'][0]).encode("utf-8")
            usernameObj = db.Test.User.find_one(
                {'user.username':username}
            )
            if usernameObj == None:
                raise Exception('Wrong Username')     
            pwHashed = usernameObj['user']['password']
            matched = bcrypt.checkpw(password, pwHashed)
            if matched:
                message = 'Login'
                teamID = str(usernameObj['user']['team'])
                req = str(usernameObj['_id'])
            else:
                message = 'Wrong Password'
                req = None
    except Exception as err:
            statusCode = 440
            message='something went wrong finding: ' + err.args[0]
    res.update({'statusCode' : statusCode,
                'message' : message,
                'teamID' : teamID,
                'currentUserID' : req
                })
    return JsonResponse(res)

@csrf_exempt
def editProfile(request):
    res={}
    message=''
    statusCode = 200

    if request.method == "PUT":
        try :
            body=dict(QueryDict(request.body))

            _id = str(body['_id'][0])

            usernameObj = db.Test.User.find_one(
                {'_id':ObjectId(_id)}
            )
            
            if usernameObj == None:
                raise Exception('Can\'t find this user')

            db.Test.User.update_one(
                {'_id':ObjectId(_id)},
                { '$set':
                    {
                    'user.bio' : str(body['bio'][0]),
                    'user.rank' : str(body['rank'][0]),
                    }
                }
            )
            message = 'Profile update success'
        except Exception as err:
            statusCode = 440
            message='something went wrong : ' + err.args[0]
    
    res.update({'statusCode' : statusCode,
                'message' : message,
                })
    return JsonResponse(res)

            
            
def getUserInfoByID(request,pk):
    res={}
    message=''
    statusCode = 200
    reqUserInfo = {}
    if request.method == 'GET':
        try:
            userInfoObj = db.Test.User.find_one(
                {'_id':ObjectId(pk)},
            )
            if userInfoObj == None:
                raise Exception('Can\'t find this member')

            reqUserInfo['_id'] = str(userInfoObj['_id'])
            reqUserInfo['username'] = str(userInfoObj['user']['username'])
            reqUserInfo['bio'] = str(userInfoObj['user']['bio'])
            reqUserInfo['rank'] = str(userInfoObj['user']['rank'])
            reqUserInfo['team'] = str(userInfoObj['user']['team'])
            
        except Exception as err:
            statusCode = 440
            message='something went wrong finding user: ' + err.args[0]
        
        res.update({ 'statusCode' : statusCode,
                     'message' : message,
                      'userInfo' : reqUserInfo
        })

        return JsonResponse(res)


def getUserInfoByName(request,pk):
    res={}
    message=''
    statusCode = 200
    reqUserInfo = {}
    if request.method == 'GET':
        try:
            userInfoObj = db.Test.User.find_one(
                {'user.username':pk},
            )
            if userInfoObj == None:
                raise Exception('Can\'t find this member')

            reqUserInfo['_id'] = str(userInfoObj['_id'])
            reqUserInfo['username'] = str(userInfoObj['user']['username'])
            reqUserInfo['bio'] = str(userInfoObj['user']['bio'])
            reqUserInfo['rank'] = str(userInfoObj['user']['rank'])
            reqUserInfo['team'] = str(userInfoObj['user']['team'])
            
        except Exception as err:
            statusCode = 440
            message='something went wrong finding user: ' + err.args[0]
        
        res.update({ 'statusCode' : statusCode,
                     'message' : message,
                      'userInfo' : reqUserInfo
        })

        return JsonResponse(res)

