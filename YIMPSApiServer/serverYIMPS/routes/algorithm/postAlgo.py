import requests
from requests.api import post
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
             }
def mergeSortForDic(myList):
    if len(myList) > 1:
        mid = len(myList) // 2
        left = myList[:mid]
        right = myList[mid:]

        mergeSortForDic(left)
        mergeSortForDic(right)

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

def sortPostBy(method,postArr):
    if method == 'rank':
        testdic = postArr
        data=testdic['allPosts']
        print(data)
        mergeSortForDic(data)
        print(data) 
        return data