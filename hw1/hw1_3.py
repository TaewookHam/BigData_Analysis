import re
import sys
import os 
import numpy as np
import time
# start = time.time()

k=3
band=6
r=20
# function distinguish n is prime number or not
def is_Prime(n):
    for i in range(2,n):
        if n%i==0:
            return 0
    return 1
# function that searches first prime number more than n
def first_Prime_over_n(n):
    n = n+1
    while is_Prime(n)==0:
        n+=1
    return n
# hash function
def hash_function(a,b,c,x):
    return (a*x + b)%c

def nC2(arr):
    aList = []
    for i in range(len(arr)):
        for j in arr[i + 1:]:
            if arr[i]<j:
                aList.append((int(arr[i]), int(j)))
            else:
                aList.append((int(j), int(arr[i])))
    return aList
# compare similarity in a band
def compare_Jaccard_cand(sig_Arrs3):
    aSet =set()
    for i in range(band):
        mat = sig_Arrs3[i]
        mat = mat.T #by T, row is doc, col is hash_func
        # In a mat, a vector consists of 20 components and it means 20 hashed values in a document
        # In doc compare Jaccard
        for i in range(mat.shape[0]):
            for j in range(i+1,mat.shape[0]):
                if np.array_equal(mat[i],mat[j]):
                    aSet.add((i,j))
    return aSet

#each shingle's row number
shingles_Dict = {}
#article's ID
article_Id_Array = np.array([])

input = sys.argv[1]
f = open(input,'r')
count = 0 # number which will be assigned and 1 will be added for next one
while True:
    line = f.readline()
    if not line:
        break
    #Extract article IDs
    article_Id_Array = np.append(article_Id_Array, line.split()[0])
    str = line.replace(line.split()[0]+' ', '').lower()
    str = re.sub(r"[^a-z\s]", "", str)
    str = re.sub(r"\s+", " ", str)
    # assign row number for each shingle
    for i in range(len(str)-k+1):
        shingle = str[i:i+3]
        # enroll the shingle in the shingles_Dict
        if shingle not in shingles_Dict.keys():
            shingles_Dict[shingle] = count
            count +=1
        else:
            pass
n = len(shingles_Dict)
f.close()

# A ndArray containing ndArrays of each document
vec_Arrs = np.array([]) 
c = first_Prime_over_n(n)
f = open(input,'r')
while True:
    #for each document
    line = f.readline()
    if not line:
        break
    str = line.replace(line.split()[0]+' ', '').lower()
    str = re.sub(r"[^a-z\s]", "", str)
    str = re.sub(r"\s+", " ", str)
    
    vec_Arr = np.array([])
    #check shingle for every document
    for shingle in shingles_Dict.keys():
        value = shingles_Dict[shingle]
        if shingle in str:
            vec_Arr = np.append(vec_Arr,1)
        else:
            vec_Arr = np.append(vec_Arr,0)
    vec_Arrs = np.append(vec_Arrs,vec_Arr)
vec_Arrs = vec_Arrs.reshape(len(article_Id_Array),n)
f.close()

vec_Hashes= np.array([])
for i in range(band*r):
    hashed_permutation = np.array([])
    a = np.random.randint(1,c-1)
    b = np.random.randint(1,c-1)
    for value in shingles_Dict.values():
        if hash_function(a,b,c,value) ==0:
            # if hash value is 0, put -1 instead of 0 to avoid confusion
            # when I use dot multiplication
            hashed_permutation = np.append(hashed_permutation,-1)
        else:
            hashed_permutation = np.append(hashed_permutation,hash_function(a,b,c,value))
    vec_Hashes = np.append(vec_Hashes, hashed_permutation)
vec_Hashes = vec_Hashes.reshape(band*r, n)


sig_Arrs = np.array([])

for vec_Hash in vec_Hashes:
    sig_Arr = np.array([])
    for vec_Arr in vec_Arrs:
        mul_Arr = np.multiply(vec_Arr,vec_Hash)
        min_val = np.min(mul_Arr[mul_Arr!=0])
        if min_val == -1:
            sig_Arr = np.append(sig_Arr,0)
        else: 
            sig_Arr = np.append(sig_Arr,min_val)
    sig_Arrs= np.append(sig_Arrs,sig_Arr)
#If we transpose it, we can cut in band more easily
sig_Arrs2=sig_Arrs.reshape(band*r,len(article_Id_Array)).T

sig_Arrs3=sig_Arrs.reshape(band,r,len(article_Id_Array))

# For candidates in LSH, compute real Jaccard by minhash value
# then print the result
res_Set = set()
for pair in compare_Jaccard_cand(sig_Arrs3):
    sub = sig_Arrs2[pair[0]] - sig_Arrs2[pair[1]]
    count_0 = list(sub).count(0)
    if float(count_0)/float(band*r) >= 0.9:
        res_Set.add((pair[0],pair[1]))
        print( article_Id_Array[pair[0]]+'\t'+article_Id_Array[pair[1]])
    else:
        pass

# print("time :", time.time() - start)