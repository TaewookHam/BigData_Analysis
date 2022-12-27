import sys
import math
import numpy as np

# userid, movieid, rating, timestamp
# function changes data type in List
def str_to_datatype(aList):
    return list([int(aList[0]), int(aList[1]),float(aList[2]),int(aList[3])])

# find row/col avg and make normalized_M
def normalize_utilitymatrix(matrix):
    normalized_M = matrix.copy()
    # subtract by avg.ratings of users
    row_avg_Array = np.array([])
    for row in normalized_M:
        count = np.count_nonzero(row)
        if count == 0:
            row_avg_Array = np.append(row_avg_Array,0)
            continue
        sum = np.sum(row)
        avg = float(sum)/count
        row_avg_Array = np.append(row_avg_Array,avg)
        row[row!=0] -= avg
    # subtract by avg.ratings of items
    col_avg_Array = np.array([])
    normalized_M = normalized_M.T # now, item is on the row side
    for row in normalized_M:
        count = np.count_nonzero(row)
        if count == 0:
            col_avg_Array = np.append(col_avg_Array,0)
            continue
        sum = np.sum(row)
        avg = float(sum)/count
        col_avg_Array = np.append(col_avg_Array,avg)
        row[row!=0] -= avg
    return normalized_M.T,row_avg_Array,col_avg_Array # return user x movie matrix by transpose and average

# construct matrix U(n x d matrix), V(d x m matrix)
# I will fill U and V with random value between 0 and 1 
def constructUV(d,normalized_M):
    row = normalized_M.shape[0]
    col = normalized_M.shape[1]
    U = np.random.rand(row,d)
    V = np.random.rand(d,col)
    return U,V

# optimize U and V to predict M as P
def optimizeUV(U,V,M,k):
    #optimize U
    for r in range(len(U)):
        for s in range(k):
            U[r][s] = np.matmul(V[s],np.subtract(M[r],np.matmul(np.delete(U,s,axis=1)[r],
            np.delete(V,s,axis=0))))/ np.sum(np.square(V[s]))
    #optimize V
    for r in range(k):
        for s in range(V.shape[1]):
            V[r][s] = np.matmul(U[:,r],np.subtract(M[:,s],np.matmul(np.delete(U,r,axis=1),
            np.delete(V,r,axis=0)[:,s]))) / np.sum(np.square(U[:,r]))
    return U,V,np.matmul(U,V)

# reconstruct normalized matrix to original scale matrix 
def reconstructP(P,row_avg_Array,col_avg_Array):
    for col in range(P.shape[1]):
        P[:,col] += col_avg_Array[col]

    for row in range(P.shape[0]):
        P[row,:] += row_avg_Array[row]
    return P

input = sys.argv[1]
f = open(input,'r')
# make quad pairs and append to total list
total = list()
while True:
    line = f.readline()
    if not line:
        break
    record = str_to_datatype(line.split(','))
    total.append(record)
f.close()
row = 672
col = 163949
# construct matrix M
def make_M(list):
    M = np.zeros((row,col))
    for record in list:
        M[record[0]-1, record[1]-1] = record[2]
    return M

avg_P = np.zeros((row,col))
# simple K-fold K = 4
# 89992/4 = 22498
for i in range(4):
    quad = 22498
    train = total[0:quad*i]+total[quad*i+quad::]
    M = make_M(train)
    # execture UV decomposition and construct P = UV
    normalized_M, row_avg_Array,col_avg_Array = normalize_utilitymatrix(M)
    U,V = constructUV(2,normalized_M)
    for i in range(2):
        U,V,P = optimizeUV(U,V,normalized_M,2)
    expected_P = reconstructP(P,row_avg_Array,col_avg_Array)
    avg_P = avg_P+expected_P
avg_P = avg_P/4

# function that changes dtype str into int
def str_to_datatype_for_test(aList):
    return list([int(aList[0]), int(aList[1]),aList[3]])

test = sys.argv[2]
f = open(test,'r')
# make output file
o = open('output.txt','w')
while True:
    line = f.readline()
    if not line:
        break
    record = str_to_datatype_for_test(line.split(','))
    o.write(str(record[0])+',')
    o.write(str(record[1])+',')
    
    ratings = avg_P[record[0]-1, record[1]-1]
    # the max value is 5.0 and min value is 0.5
    if ratings > 5.0:
        ratings = 5
    elif ratings < 0.5:
        ratings = 0.5
    o.write(str(ratings) + ',')
    o.write(record[-1])
o.close()
f.close()