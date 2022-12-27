import sys
import numpy as np

# userid, movieid, rating, timestamp
# function that changes str to specific data type
def str_to_datatype(aList):
    return list([int(aList[0]), int(aList[1]),float(aList[2]),int(aList[3])])

input = sys.argv[1]
f = open(input,'r')
# construct utility matrix M
row = 672
col = 164979
M = np.zeros((row,col))
while True:
    line = f.readline()
    if not line:
        break
    record = str_to_datatype(line.split(','))
    M[record[0]-1, record[1]-1] = record[2]

# function that finds each user's avg and make normalized_M
def normalize_utilitymatrix(matrix):
    normalized_M = matrix.copy()
    # avg_M = np.array([])
    for row in normalized_M:
        count = np.count_nonzero(row)
        if int(count) == 0:
            continue
        sum = np.sum(row)
        avg = float(sum)/count
        row[row!=0] -= avg
    return normalized_M
# function that find similar users with User id 600
def find_similar_users(matrix,User_U):
    normalized_mat = matrix.copy()
    # to compute cosine
    for row in normalized_mat:
        if np.linalg.norm(row) != 0:
            row /= np.linalg.norm(row)
    mul = np.matmul(normalized_mat,User_U.T)
    top10 = mul.argsort()[::-1][1:11]# 1:11 because we except the User_U itself
    return top10 #it is user_index not id

def avg_ratings_I(top10_array,matrix):
    similar_user_I = matrix[top10_array,0:1000]
    return similar_user_I

# function that calculate avg of items and returns ndarray
def get_avg_ofItems(matrix):
    res = np.array([])
    I = matrix.copy().T
    # item is now in row direction
    for row in I:
        count = np.count_nonzero(row)
        if count == 0:
            res = np.append(res,0)
            continue
        sum = np.sum(row)
        avg = float(sum)/count
        res = np.append(res,avg)
    return res
# function that gets the top5 movies based on user-user
def get_top5_userbase(top10_I):
    res = get_avg_ofItems(top10_I)
    top_index = res.argsort()[::-1][0:20]
    aList = []
    for index in top_index:
        aList.append((index,res[index]))
    sorted_list = sorted(aList,key=lambda x: x[0],reverse=False)
    sorted_list2 = sorted(sorted_list,key=lambda x: x[1],reverse = True)
    for pair in sorted_list2[0:5]:
        print(str(pair[0]+1) + '\t'+ str(pair[1]))
    return

# save original M to use it later when predicting the ratings
original_M = M.copy()
# save normalized M to use repeatedly
normalized_M = normalize_utilitymatrix(M)

# procedure to find userbase top5 movies
similar_user_top10 = find_similar_users(normalized_M,normalized_M[599])
top10_I = avg_ratings_I(similar_user_top10,original_M)
get_top5_userbase(top10_I)

# funtion that find similar items with I(1~1000) and return the dictionary
# input is normalized matrix
def find_similar_items(matrix):
    normalized_mat = matrix.T.copy() # now item is on the rows
    # to compute cosine
    for row in normalized_mat:
        if np.linalg.norm(row) != 0:
            row /= np.linalg.norm(row)
    sim_items = dict()
    for i in range(1000):
        # find similar movie except id 1~1000
        mul = np.matmul(normalized_mat[1000::],normalized_mat[i].T)
        top10 = mul.argsort()[::-1][0:10] # it represent index, not id
        sim_items[i] = top10 + 1000 # add 1000 due to the indexing[1000::]
    return sim_items

# function that get the top5 based on item-item
def get_top5_itembase(dict,original_M):
    res = np.array([])
    for movie in dict.keys():
        row = original_M[599][dict[movie]] #movieID 1001~
        count = np.count_nonzero(row)
        if int(count) == 0:
            res = np.append(res,0)
            continue
        sum = np.sum(row)
        avg = float(sum)/count
        res = np.append(res,avg)
    top_index = res.argsort()[::-1][0:20]
    aList = []
    for index in top_index:
        aList.append((index,res[index]))
    sorted_list = sorted(aList,key=lambda x: x[0],reverse=False)
    sorted_list2 = sorted(sorted_list,key=lambda x: x[1],reverse = True)
    for pair in sorted_list2[0:5]:
        print(str(pair[0]+1) + '\t'+ str(pair[1]))
    return
# procedure to find itembase top5 movies
dict = find_similar_items(normalized_M)
get_top5_itembase(dict,original_M)

