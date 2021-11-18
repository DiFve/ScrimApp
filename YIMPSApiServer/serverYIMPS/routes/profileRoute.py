from django.http import JsonResponse,QueryDict
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from utils import get_db_handle
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
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
            user = {
                'username': body['username'][0],
                'password': body['password'][0],
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