class MatchPriorityNode:
    def __init__(self,obj,priorityValue):
        self.priorityValue = priorityValue
        self.obj = obj
    
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
        while (index > 0 and self.getPriorityValue(self.match[self.parent(index)]) < self.getPriorityValue(self.match[index])) :
            self.swap(self.parent(index), index)
            index = self.parent(index)

    def shiftDown(self,index) :
        maxIndex = index
        l = self.leftChild(index)
        if (l <= self.size and self.getPriorityValue(self.match[l]) > self.getPriorityValue(self.match[maxIndex])) :
            maxIndex = l
        r = self.rightChild(index)
        if (r <= self.size and self.getPriorityValue(self.match[r]) > self.getPriorityValue(self.match[maxIndex])) :
            maxIndex = r
        if (index != maxIndex) :
            self.swap(index, maxIndex)
            self.shiftDown(maxIndex)
         
    def changeDateToPriorityValue(self,date):
        year = date[2]
        month = date[1]
        day = date[0]
        pv = (year*10000)+(month*100)+day
        return pv

    def insert(self,obj,lists) :
        pv = self.changeDateToPriorityValue(lists)
        self.size = self.size + 1
        self.match[self.size] = MatchPriorityNode(obj,pv)
        self.shiftUp(self.size)
   
    def extractMax(self) :
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
   
    def getMax(self) :
        return self.match[0]
   
    def Remove(self,i) :
        self.match[i] = self.getMax() + 1
        self.shiftUp(i)
        self.extractMax()
   
    def printQueue(self):
        i = 0 
        while (i<=self.size):
            print(self.match[i].obj,end = " ")
            i += 1

q = matchPriorityQueue()
# Insert the element to the
# priority queue
q.insert(45,[3,5,2021])
q.insert(20,[4,10,2002])
q.insert(14,[1,2,1111])
q.insert(12,[9,9,2019])
q.insert(31,[12,12,2011])
q.insert(7,[1,2,2211])
q.insert(11,[2,1,9999])
q.insert(13,[3,5,1444])
q.insert(7,[1,1,2001])
   
q.printQueue()
# Node with maximum priority
print("Node with maximum priority :" ,  q.extractMax())
q.printQueue()
'''

# Priority queue after extracting max
print("Priority queue after extracting maximum : ", end = "")
j = 0
while (j <= size) :
 
    print(H[j], end = " ")
    j += 1
   
print()
   
# Change the priority of element
# present at index 2 to 49
changePriority(2, 49)
print("Priority queue after priority change : ", end = "")
k = 0
while (k <= size) :
 
    print(H[k], end = " ")
    k += 1
   
print()
   
# Remove element at index 3
Remove(3)
print("Priority queue after removing the element : ", end = "")
l = 0
while (l <= size) :
 
    print(H[l], end = " ")
    l += 1
     
    # This code is contributed by divyeshrabadiya07.
'''