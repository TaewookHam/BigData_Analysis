import sys
import math
import numpy as np

# Preparing for the given settings
stream = sys.argv[1]
k_values = np.array([],dtype=int)
M=0

for arg in sys.argv[2:]:
   k_values = np.append(k_values,int(arg))
   M +=1

N = 10000000
Timestamp = 0
numofBuckets = int(math.ceil(math.log(N, 2)))

bucket_List = []
for i in range(numofBuckets):
    bucket_List.append([])

# Fuction that updates the buckets
def updateList(bucket_List):
    for i in range (len(bucket_List)):
        if len(bucket_List[i]) > 2:
            bucket_List[i].pop(0)
            bucket_List[i+1].append(bucket_List[i].pop(0))

# Read stream and update bucket_List if read 1
f = open(stream,'r')
while True:
    line = f.readline()
    if not line:
        break
    num = int(line.rstrip('\n'))
    Timestamp = (Timestamp + 1) % (N+1)
    if num == 1:
        bucket_List[0].append(Timestamp)
        updateList(bucket_List)
    else:
        pass
f.close()


# Sort each bucket to order in descending order
numof_filledbuckets = 0
for bucket in bucket_List:
    if bucket:
        bucket.sort(reverse=True)
        numof_filledbuckets+=1
print(bucket_List)
# fuction that estimate the sum of ones
# if j is 1, it means estimate range covers the first bucket of two buckets whose size is power
def getSum(bucket_List,power,j):
    sum =0
    if j==1:
        for i in range(power):
            sum += len(bucket_List[i])*math.pow(2,i)
        sum += math.pow(2,power)/float(2)
    if j==0:
        for i in range(power):
            sum += len(bucket_List[i])*math.pow(2,i)
        sum -= math.pow(2,power-1)/float(2)
    return sum

for k in k_values:
    Escape = True # bool to break double loop
    
    # If k contains no 1 
    if bucket_List[0][0]<N+1-k :
        print(0)
        continue
    
    # Usual case, estimate the num of 1's
    for i in range(len(bucket_List)):
        for j in range(len(bucket_List[i])):
            if N-k+1 > bucket_List[i][j]:
                print(getSum(bucket_List,i,j))
                Escape = False
                break
        if Escape==False:
            break

        # If k range covers the very earliest filled buecket
        if i == numof_filledbuckets:
            if j==1:
                print(getSum(bucket_List,i-1,j) + (math.pow(2,i-1)))
            if j==0:
                print(getSum(bucket_List,i-1,j))
