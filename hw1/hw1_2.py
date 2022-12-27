import re
import sys
import os 
import numpy as np
import time
start = time.time()
threshold = 200
#function that makes combination
def nC2(arr):
    aList = []
    for i in range(len(arr)):
        for j in arr[i + 1:]:
            if arr[i]<j:
                aList.append((int(arr[i]), int(j)))
            else:
                aList.append((int(j), int(arr[i])))
    return aList

# fucntion that searchs the pairs in each lines 
#and return all frequency if over threshold, or returns 0
def search(item1,item2,threshold,hashed_basket):
    n=0
    for hashed_basket_List in hashed_basket:
        if item1 in hashed_basket_List:
            if item2 in hashed_basket_List:
                n+=1
            else:
                pass
        else:
            pass
    if n>=threshold:
        return n
    else: 
        return 0

input = sys.argv[1]
item_freq={} # How many times each item appears 
table_1={} # items hashing dictionary
table_2={} # hashing dictionary which contains number of items over the threshold
basket = []
hashed_basket=[]

f = open(input,'r')
while True:
    line = f.readline()
    if not line:
        break
    basket_List = line.strip().split(' ')
    #basket.txt -> make list in list
    basket.append(basket_List)
    hashed_basket_List = []
    #to know Number of frequent items
    for item in basket_List:
        if item in table_1.keys():
            item_freq[table_1[item]]+=1    
        else:
            table_1[item] = len(table_1)
            item_freq[table_1[item]] = 1
        # translate item names to integer and make each line of basket.txt(cosinst of integer)
        hashed_basket_List.append(int(item.replace(item,str(table_1[item]))))
    hashed_basket.append(hashed_basket_List)
f.close()


over_200_Dict = dict(filter(lambda pair: pair[1]>=threshold, item_freq.items()))

# print(over_200_Dict)
for key in over_200_Dict.keys():
    #assign from 1 to m
    table_2[key] = (len(table_2)+1)

inv_table_2 = {v:k for k,v in table_2.items()}

# # triangular matrix
# # using matrix
m= len(inv_table_2)
mat = np.zeros([m-1,m-1])
res_Dict = {}
for pair in nC2(inv_table_2.keys()):
    item1 = pair[0] #1
    item2 = pair[1] #2

    n = search(inv_table_2[item1],inv_table_2[item2],threshold,hashed_basket)
    row = int(item2)-int(2)
    col = int(item1)-int(1)
    mat[row][col] = n

inv_table_1 = {v:k for k,v in table_1.items()}
res = {}
for i in range(m-1): #col 0 ~ m-2
    for j in range(0+i,m-1): #row 0 ~m-2
        if mat[j][i]>=threshold:
            v = mat[j][i]
            item2 = j+int(2)
            item1 = i+int(1)
            a = inv_table_1[inv_table_2[item1]] #16
            b = inv_table_1[inv_table_2[item2]] #5
            res[(a,b)] = int(v)

res = sorted(res.items(), key=lambda x: x[1], reverse=True)

print(len(table_2))
print(len(res))
n=0
for pair in res:
    k = pair[0]
    v = pair[1]
    print(str(k[0])+'\t'+str(k[1])+'\t'+str(v))
    n +=1
    if n==10:
        break

print("time :", time.time() - start)










