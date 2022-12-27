import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)

import time
start = time.time()

#function which execute combination nC2
def nC2(arr):

    aList = []
    for i in range(len(arr)):
        for j in arr[i + 1:]:
            if arr[i]<j:
                aList.append((int(arr[i]), int(j)))
            else:
                aList.append((int(j), int(arr[i])))
    return aList

def make_pairs(line):
    token=line.split()
    #No connected friends
    id = int(token[0])
    if len(token) ==1:
        friends = [-1]
    else:
        friends = list(map(lambda x: int(x), token[1].split(',')))
    return id, friends

def make_friends(token):
    id = token[0] # int id
    friends = token[1] # list friends
    pairs = []
    #who are already friend
    for friend in friends:
        if id<friend:
            key = (id,friend)
        else:
            key = (friend,id)
        pairs.append((key,0))

    if len(friends)==1 :
        return [((-1,-1),1)]
    #pair them as ((A,C) , 1), they are candidates who can know each other,
    for mute_friend in nC2(friends):
        key = (mute_friend[0],mute_friend[1])
        pairs.append((key,1))
    return pairs

lines = sc.textFile(sys.argv[1])
pairs = lines.map(make_pairs)
network_b = pairs.flatMap(make_friends).filter(lambda x: x[0][0] != -1)

#reduceByKey & filter candidates who are already friends

filtered_b = network_b.groupByKey().filter(lambda x: 0 not in x[1]).map(lambda pair:(pair[0], sum(pair[1])))

top10_List = filtered_b.sortByKey().takeOrdered(10, key = lambda x: -x[1])
for ranker in top10_List:
    print( str(ranker[0][0]) + '\t' + str(ranker[0][1])+'\t'+str(ranker[1]))
print("time :", time.time() - start)