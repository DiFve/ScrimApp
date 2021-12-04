from django.http import JsonResponse,QueryDict
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from dns.rdatatype import NINFO
from pymongo.read_preferences import _invalid_max_staleness_msg
from utils import get_db_handle
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
import json
import bcrypt
import gridfs
import base64
import json
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
            
            idObj = db.Test.User.find_one(
                {
                    'user.username' : username
                }
            )
            print(idObj)
            profilePic =b'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'
            fs = gridfs.GridFS(db.grid_file)
            fs.put(profilePic, filename = str(idObj['_id']))

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
            message='something went wrong : ' + str(err.args[0])
    
    res.update({'statusCode' : statusCode,
                'message' : message,
                })
    return JsonResponse(res)
@csrf_exempt
def setProfileImage(request):
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
            
            data = body['pictureProfile'][0].encode('utf-8')
            
            fs = gridfs.GridFS(db.grid_file)
            isExist = db.grid_file.fs.files.find_one(
                {'filename': _id}
            )
            print(isExist)
            if isExist != None:
                fs.delete(isExist['_id'])
            fs.put(data, filename = _id)
            message = 'Picture profile update success'
        except Exception as err:
            statusCode = 440
            message='something went wrong : ' + str(err.args[0])
    
    res.update({'statusCode' : statusCode,
                'message' : message,
                })
    return JsonResponse(res)   


def getProfileImage(request,pk):
    res={}
    message=''
    image = ''
    statusCode = 200    
    if request.method == 'GET':
        try:

            data = db.grid_file.fs.files.find_one(
                {'filename':pk}
            )

            my_id = data['_id']
            image =  gridfs.GridFS(db.grid_file).get(my_id).read()
            image = base64.decodebytes(image)
            image = str(base64.b64encode(image))
            image = image[2:-1]

            # image = image.encode('utf-8')
            # image = base64.decodebytes(image)
            
            
            # download = 'D:/Datastructure_project/ScrimApp/YIMPSApiServer/serverYIMPS/routes/monnnnnika.png'
            # output = open(download, 'wb')
            # output.write(image)
            # output.close()
            
        except Exception as err:
            statusCode = 440
            message='something went wrong finding user: ' + err.args[0]
        
        res.update({ 'statusCode' : statusCode,
                    'message' : message,
                    'image' : image
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

