import sys
import numpy as np
import math

features = sys.argv[1]
labels = sys.argv[2]

row = 6000
col = 122
C = 0.7
eta = 0.001
# C = 0.7 eta = 0.001, b= 0 -> 0.83xxx

# function that reads vectors from features.txt and return feature array
def make_Features(input):
    res = np.array([],dtype=int)
    f = open(input,'r')
    while True:
        line = f.readline()
        if not line:
            break
        arr = np.array([],dtype=int)
        aList = line.split(',')
        for num in aList:
            arr=np.append(arr, int(num))
        arr = np.append(arr,1)
        res = np.append(res,arr)
    res = res.reshape(row,col+1)
    f.close()
    return res

# function that reads vectors from labels.txt and return label array
def make_Labels(input):
    res = np.array([],dtype=int)
    f = open(input,'r')
    while True:
        line = f.readline()
        if not line:
            break
        res=np.append(res, int(line))
    f.close()
    return res

# function that trains/edits w and then, return next w and its correctness
def train(row,features,labels,w,C):
    mul = np.matmul(features,w)
    wrong = np.zeros((row,col+1))
    answer_sum = 0
    for i in range(row):
        if labels[i]==1:
            if mul[i] >= 1:
                answer_sum +=1
            else:
                for j in range(col+1): # col is 122: j:0~122
                    wrong[i][j] = -1*features[i][j]
        else : # if labels[i]==-1
            if mul[i] <= -1:
                answer_sum +=1
            else:
                for j in range(col+1):
                    wrong[i][j] = -(-1)*features[i][j]
    # calculate next editted w
    edited_vec = np.array([])
    for k in range(col+1):
        # update 
        derivative = w[k] + C*(sum(wrong[:,k]))
        edited_vec = np.append(edited_vec,w[k] - eta*(derivative))
    return edited_vec, float(answer_sum)/row

# function that return the correctness of the model 
def validate(row,features,labels,w):
    mul = np.matmul(features,w)
    answer_sum = 0
    for i in range(row):
        if labels[i]==1:
            if mul[i] >= 0:
                answer_sum +=1
            else:
                continue
        else : # if labels[i]==-1
            if mul[i] <= 0:
                answer_sum +=1
            else:
                continue
    return float(answer_sum)/row

F = list(make_Features(features))
L = list(make_Labels(labels).reshape(row,1))

avg = 0
# K-fold K = 10
for i in range(10):
    # generate w and train,validation sets
    w = np.zeros(col)
    w = np.append(w,0)
    portion = 600
    X_tr = F[0:portion*i]+F[(portion*i+portion)::]
    Y_tr = L[0:portion*i]+L[(portion*i+portion)::]

    X_val = F[portion*i:portion*i+portion]
    Y_val = L[portion*i:portion*i+portion]

    X_tr_row = 5400
    X_val_row = 600

    max_cand = np.array([],dtype=float)
    max_w_cand = np.array([])
    # iterate n times for descent gradient 
    # and take editted w when the probability becomes highest by iterating n times
    for i in range(30): # n=30 it's my mind
        w_old = w
        w,proba = train(X_tr_row,X_tr,Y_tr,w,C)

        max_cand = np.append(max_cand,proba)
        max_w_cand = np.append(max_w_cand,w_old)
    max_w_cand = max_w_cand.reshape(30,123)
    w = max_w_cand[np.argmax(max_cand)]

    p = validate(X_val_row,X_val,Y_val,w)

    # print('Global max: %f'%(p))
    avg += p 
print(avg/10)
print(C)
print(eta)
