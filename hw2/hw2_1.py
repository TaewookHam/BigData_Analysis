import re
import sys
import numpy as np
from pyspark import SparkConf, SparkContext
import time
start = time.time()
conf = SparkConf()
sc = SparkContext(conf=conf)

# function that change type str to float in aList
def str_to_float(aList):
    vec = list(map(float,aList))
    return np.array(vec)

# make vectors of each point in the array vec_Arr
row = 4601
col = 58

f = open(sys.argv[1],'r')
vec_Arr = np.array([])
while True:
    line = f.readline()
    if not line:
        break
    vec = str_to_float(line.split())
    vec_Arr = np.append(vec_Arr,vec)
vec_Arr = vec_Arr.reshape(row,col)
f.close()
# initial k-point
first_Point = vec_Arr[0]
k = int(sys.argv[2])

# function that calculate distance
def cal_dist(vec1,vec2):
    return np.linalg.norm(vec1-vec2)

# list of k-fixed point, points in this list will be the centroids
k_Points = []
k_Points.append(first_Point)

# Procedure of Finding k-points
# A point has the distance integers from k-points as an array of length k. 
# The largest value among the collections of minimum values in each points array becomes the next k-point.
dist_Arrs = np.array([])
for i in range(k-1):
    dist_Arr=np.array([])
    for vec in vec_Arr:
        dist_Arr = np.append(dist_Arr, cal_dist(k_Points[i],vec))
    dist_Arrs = np.append(dist_Arrs,dist_Arr).reshape(i+1,row).T
    min_Arr=np.array([])
    for j in range(row):
        min_Arr = np.append(min_Arr,np.min(dist_Arrs[j]))
    max = np.argmax(min_Arr)
    k_Points.append(vec_Arr[max])
    dist_Arrs = dist_Arrs.T

# function that finds the nearest centroid
def find_closest_centroid(vec):
    dist_Arr=np.array([])
    for k_point in k_Points:
        dist_Arr = np.append(dist_Arr,cal_dist(k_point,vec))
    centroid  = np.argmin(dist_Arr)
    return (centroid,vec)

# function that find a cluster's diameter
def find_diameter(vec_Arr):
    max = 0
    for vec_i in vec_Arr:
        for vec_j in vec_Arr:
            if (cal_dist(vec_i,vec_j))>max:
                max = cal_dist(vec_i,vec_j)
    return max

# make clusters by using Spark
lines = sc.textFile(sys.argv[1])
vec_Rdd = lines.map(lambda l: l.split()).map(str_to_float)
cluster = vec_Rdd.map(find_closest_centroid).groupByKey().map(lambda pair: pair[1])

# find each cluster's diameter and calculate the avg
diameter_avg = (cluster.map(find_diameter).reduce(lambda a,b: a+b)) / float(k) 
print(diameter_avg)
