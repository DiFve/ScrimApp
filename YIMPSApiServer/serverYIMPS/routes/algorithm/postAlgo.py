import requests
from requests.api import post
import math
rank={
              'Iron1': 0,
              'Iron2': 1,
              'Iron3': 2,
              'Bronze1' : 3,
              'Bronze2' : 4,
              'Bronze3' : 5,
              'Silver1' : 6,
              'Silver2' : 7,
              'Silver3' : 8,
              'Gold1' : 9,
              'Gold2' : 10,
              'Gold3' : 11,
              'Platinum1' : 12,
              'Platinum2' : 13,
              'Platinum3' : 14,
              'Diamond1' : 15,
              'Diamond2' : 16,
              'Diamond3' : 17,
              'Immortal1' : 18,
              'Immortal2' : 19,
              'Immortal3' : 20,
              'Radiant' : 21,
              '':22,
              'No information':23,
             }
def mergeSortRank(myList):
    if len(myList) > 1:
        mid = len(myList) // 2
        left = myList[:mid]
        right = myList[mid:]

        mergeSortRank(left)
        mergeSortRank(right)

        i = 0
        j = 0
        
        k = 0
        
        while i < len(left) and j < len(right):
            if rank[left[i]['teamRank']] <= rank[right[j]['teamRank']]:
              myList[k] = left[i]
              i += 1
            else:
                myList[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            myList[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            myList[k]=right[j]
            j += 1
            k += 1

def mergeSortDate(myList):
    if len(myList) > 1:
        mid = len(myList) // 2
        left = myList[:mid]
        right = myList[mid:]

        mergeSortDate(left)
        mergeSortDate(right)

        i = 0
        j = 0
        
        k = 0
        
        while i < len(left) and j < len(right):
            dayL=left[i]['date'].split('/')[0]
            monthL=left[i]['date'].split('/')[1]
            yearL=left[i]['date'].split('/')[2]
            dayR = right[j]['date'].split('/')[0]
            monthR = right[j]['date'].split('/')[1]
            yearR = right[j]['date'].split('/')[2]
            if yearL<yearR:
              myList[k] = left[i]
              i += 1
            elif yearL == yearR:
                if monthL < monthR:
                    myList[k]=left[i]
                    i+=1
                elif monthR < monthL:
                    myList[k]=right[j]
                    j+=1
                else:
                    if dayL<dayR:
                        myList[k]=left[i]
                        i+=1
                    elif dayL > dayR:
                        myList[k]=right[j]
                        j+=1
                    else:
                        hrL = left[i]['time'].split(':')[0]
                        hrR = right[i]['time'].split(':')[0]
                        minL = left[i]['time'].split(':')[1]
                        minR = right[i]['time'].split(':')[1]
                        if hrL < hrR :
                            myList[k]=left[i]
                            i+=1
                        elif hrR < hrL:
                            myList[k]=right[j]
                            j+=1
                        else:
                            if minL<=minR:
                                myList[k]=left[i]
                                i+=1
                            else:
                                myList[k]=right[j]
                                j+=1
            else:
                myList[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            myList[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            myList[k]=right[j]
            j += 1
            k += 1

def sortPostBy(method,postArr):
    print(method)
    if method == 'rank':
        testdic = postArr
        data=testdic['allPosts']
        print(data)
        mergeSortRank(data)
        print(data) 
        return data
    elif method == 'date':
        testdic = postArr
        data=testdic['allPosts']
        print(data)
        mergeSortDate(data)
        print(data)
        return data
    
def findAvgRank(members):
    print(members)
    try:
        allrank=0
        for user in members:
            res=requests.get('http://34.124.169.53:8000/api/getUserInfoByID/{0}'.format(user['userid']))
            userrank=res.json()['userInfo']['rank']
            if userrank == '':
                return 'No information'
            allrank+=rank[userrank]
        avgRankInt=math.floor(allrank/len(members))

        for i in rank.keys():
            if rank[i] == avgRankInt:
                return i
    except Exception as err:
        print('some err in avg:' + err.args[0])