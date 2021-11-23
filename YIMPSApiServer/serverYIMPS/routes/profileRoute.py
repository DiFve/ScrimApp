from django.http import JsonResponse,QueryDict
from django.http.response import HttpResponse
from django.http.request import HttpRequest
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
            username = body['username'][0]
            password = str(body['password'][0]).encode("utf-8")
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
                    'req':[],
                }
            )
            message = 'successfully'

        except Exception as err:
            statusCode = 440
            message='something went wrong saving: ' + err.args[0]
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
                req = str(usernameObj['_id'])
                print("Login!!")
            else:
                message = 'Wrong Password'
                req = None
                print("Wrong Password")
    except Exception as err:
            statusCode = 440
            message='something went wrong finding: ' + err.args[0]
    res.update({'statusCode' : statusCode,
                'message' : message,
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
            
            db.Test.User.update_one(
                {'_id':ObjectId(_id)},
                { '$set':
                    {
                    'bio' : str(body['bio'][0]),
                    'rank' : str(body['rank'][0]),
                    'team' : str(body['team'][0])
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

            
            



