import sys
from pyspark import SparkConf, SparkContext
conf = SparkConf()
sc = SparkContext(conf=conf)

beta = 0.9
n = 1000
lines = sc.textFile(sys.argv[1])
pair_Rdd = lines.map(lambda l: l.split('\t')).map(lambda x: (x[0],x[1])).distinct()
# make the form ((sender,(receiver,probability))
col_vec = pair_Rdd.groupByKey().flatMap(lambda x: [(int(x[0]),(int(d),beta/len(x[1]))) for d in x[1]])
e_n_1minusbeta = sc.parallelize([(int(i),(1-beta)/n)for i in range(1,n+1)])
v = sc.parallelize([(int(i),float(1)/n) for i in range(1, n+1)])

# function that makes the form ((rowNumber,prob))
# x[1] represents value of k-v pair 
# x[1][0][0] represents row number(recevier)
# x[1][0][1] represents probabilty
# x[1][1] represents each element of v
def mul(col_vec,v):
    return col_vec.join(v).map(lambda x: (x[1][0][0], x[1][0][1]*x[1][1]) )

# function that makes next v by beta*Mv + (1-beta)e/n
def summ(mul,e):
    return mul.reduceByKey(lambda a,b: a+b).join(e).map(lambda x: (x[0],x[1][1]+x[1][0]))

# iterate twice at one time, repeat 25 time to avoid laziness of spark
for i in range(25):
    if i !=0:
        v = sc.parallelize(check_point)
    for i in range(2):
        mul_vec = mul(col_vec,v)
        v = summ(mul_vec,e_n_1minusbeta)
    check_point = v.collect()

top10 = v.takeOrdered(10, key = lambda x: -x[1])
for ranker in top10:
    print("%d\t%.5f" %(ranker[0],ranker[1]))