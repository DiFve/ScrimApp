from time import time
from datetime import date, datetime
from django.http import JsonResponse,QueryDict
from django.http.response import HttpResponse
from django.http.request import HttpRequest
import requests
from requests.sessions import TooManyRedirects
from utils import get_db_handle
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
from .algorithm import postAlgo
import json

db=get_db_handle()

class MatchPriorityNode:
    def __init__(self,obj,priorityValue):
        self.priorityValue = priorityValue
        self.obj = obj

    def __str__(self):
        return str(self.obj)
    
class matchPriorityQueue:
    def __init__(self):
        self.match = [0]*50
        self.size = -1

    def parent(self,index) :
        return (index - 1) // 2

    def leftChild(self,index) :
        return ((2 * index) + 1)
   
    def rightChild(self,index) :
        return ((2 * index) + 2)

    def getPriorityValue(self,node):
         return node.priorityValue

    def swap(self,i, j) :
        temp = self.match[i]
        self.match[i] = self.match[j]
        self.match[j] = temp

    def shiftUp(self,index) :
        while (index > 0 and self.getPriorityValue(self.match[self.parent(index)]) > self.getPriorityValue(self.match[index])) :
            self.swap(self.parent(index), index)
            index = self.parent(index)

    def shiftDown(self,index) :
        maxIndex = index
        l = self.leftChild(index)
        if (l <= self.size and self.getPriorityValue(self.match[l]) < self.getPriorityValue(self.match[maxIndex])) :
            maxIndex = l
        r = self.rightChild(index)
        if (r <= self.size and self.getPriorityValue(self.match[r]) < self.getPriorityValue(self.match[maxIndex])) :
            maxIndex = r
        if (index != maxIndex) :
            self.swap(index, maxIndex)
            self.shiftDown(maxIndex)
         
    def changeDateAndTimeToPriorityValue(self,date,time):
        matchDate = date.split("/")
        matchTime = time.split(":")
        year = int(matchDate[2])
        month = int(matchDate[1])
        day = int(matchDate[0])
        hour = int(matchTime[1])
        minute = int(matchTime[0])
        pv = (year*100000000)+(month*1000000)+(day*10000)+(hour*100)+minute
        return pv

    def insert(self,obj,date,time) :
        pv = self.changeDateAndTimeToPriorityValue(date,time)
        self.size = self.size + 1
        self.match[self.size] = MatchPriorityNode(obj,pv)
        self.shiftUp(self.size)
   
    def extractNextMatch(self) :
        result = self.match[0]
        self.match[0] = self.match[self.size]
        self.size = self.size - 1
        self.shiftDown(0)
        return result
   
    def changePriority(self,i,p) :
 
        oldp = self.match[i]
        self.match[i] = p
        if (p > oldp) :
            self.shiftUp(i)
        else :
            self.shiftDown(i)
   
    def getNextMatch(self) :
        return self.match[0]
   
    def Remove(self,i) :
        self.match[i] = self.getMin() + 1
        self.shiftUp(i)
        self.extractNextMatch()
   
    def printQueue(self):
        i = 0 
        while (i<=self.size):
            print(self.match[i],end = " ")
            i += 1
        print()

def countdown(today,nextday):
    diff = nextday - today
    if diff.days == 0:
        return "today"
    else:
        return str(diff.days) + " day"

def getNextFiveMatch(request,pk):
    res = {}
    message=''
    statuscode = 200
    try:
        if request.method == 'GET':
            listOfNextFiveMatch = []
            matchQueue = matchPriorityQueue()
            allPost = requests.get('http://34.124.169.53:8000/api/get-match/{0}'.format(pk))
            allMatch = list(allPost.json()['allUserMatches'])
            for match in allMatch:
                Detailmatch = match['postData']
                dateOfMatch = Detailmatch['date']
                timeOfMatch = Detailmatch['time']
                nextMatchDate = list(map(int,dateOfMatch.split("/")))
                nextday = datetime(nextMatchDate[2],nextMatchDate[1],nextMatchDate[0])
                Detailmatch.update({'countdown':countdown(datetime.now(),nextday)})
                matchQueue.insert(Detailmatch,dateOfMatch,timeOfMatch)
            i = 0 #indexOfMatch
            sizeOfMatch = matchQueue.size
            while i <= sizeOfMatch:
                if i >= 5:
                    break
                listOfNextFiveMatch.append(matchQueue.extractNextMatch().obj)
                i += 1
            message = 'successfully get 5 next match'
    except Exception as err:
        statuscode = 440
        message = 'something went wrong finding: ' + err.args[0]
    res.update({'statusCode':statuscode})
    res.update({'message':message})
    res.update({'nextFivePost':listOfNextFiveMatch})
    return JsonResponse(res)
    