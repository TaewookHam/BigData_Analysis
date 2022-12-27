import sys
import numpy as np
import math
import itertools
input = sys.argv[1]

def get_MaxNode(input):
    max = 0
    f = open(input,'r')
    while True:
        line = f.readline()
        if not line:
            break
        rel = line.split('\t')
        if rel[-1] != '\\N\n':
            if int(rel[0])>max:
                max = int(rel[0])
            if int(rel[1])>max:
                max = int(rel[1])
    f.close()
    return max

node = get_MaxNode(input) #63731

# take empty dictionary then make empty hash table
# x is the size
def make_HashTable(x):
    aDict = dict()
    for i in range(1,x+1):
        aDict[i]=0
    return aDict

# function that find the node degrees and edgeIndex_Pair
def part1and2(input):
    edgeIndex_Pair = dict()
    dgrs = make_HashTable(node)
    f = open(input,'r')
    while True:
        line = f.readline()
        if not line:
            break
        rel = line.split('\t')
        # if rel[-1] != '\\N\n':
        a = int(rel[0])
        b = int(rel[1])
        if a<b:
            edgeIndex_Pair[(a,b)] = 1
        else:
            edgeIndex_Pair[(b,a)] = 1
    f.close()
    for pair in edgeIndex_Pair.keys():
        dgrs[pair[0]] += 1
        dgrs[pair[1]] += 1
    for pair in edgeIndex_Pair.keys():
        if dgrs[pair[1]] < dgrs[pair[0]]:
            edgeIndex_Pair[(pair[1],pair[0])] = edgeIndex_Pair[(pair[0],pair[1])]
            del edgeIndex_Pair[(pair[0],pair[1])]
    return edgeIndex_Pair,dgrs

# function that finds the edgeIndex_Single(Which nodes are connected to 'a single node')
def part3(edgeIndex_Pair):
    edgeIndex_Single = dict()
    for i in range(1,node+1):
        edgeIndex_Single[i] = np.array([],dtype=int)
    for edge in edgeIndex_Pair:
        edgeIndex_Single[edge[0]] = np.append(edgeIndex_Single[edge[0]],edge[1])
        edgeIndex_Single[edge[1]] = np.append(edgeIndex_Single[edge[1]],edge[0])
    return edgeIndex_Single

edgeIndex_Pair,dgrs = part1and2(input) #817090
edgeIndex_Single = part3(edgeIndex_Pair)
# parameter input file
# function that finds heavy hitter triangles
def find_HH_Tri(input,dgrs,edgeIndex_Pair):
    HH_Tri = np.array([],dtype=int)
    HH_Nodes = np.array([],dtype=int)
    for node in dgrs.keys():
        if dgrs[node]>=math.sqrt(len(edgeIndex_Pair)):
            HH_Nodes = np.append(HH_Nodes,node)
    # construct triple and validate all the edges are alive
    HH_cand = itertools.combinations(HH_Nodes,3) # these are just candidates
    for cand in HH_cand:
        if (cand[0],cand[1]) in edgeIndex_Pair.keys():
            pass
        else: continue
        if (cand[1],cand[2]) in edgeIndex_Pair.keys():
            pass
        else: continue
        if (cand[0],cand[2]) in edgeIndex_Pair.keys():
            HH_Tri = np.append(HH_Tri,cand)
        else: continue
    return HH_Tri.reshape(int(len(HH_Tri)/3),3)

Ans1 = len(find_HH_Tri(input,dgrs,edgeIndex_Pair))

# function that checks the condition of v1<v2(curved <)
def check_condition(v1,v2,dgrs):
    if dgrs[v1]<=dgrs[v2]:
        if dgrs[v1]==dgrs[v2]:
            if v1<v2:
                return 1
            else: return -1
        else: return 1
    else: return -1

#function that finds other triangles
def find_Others(input,dgrs,edgeIndex_Pair,edgeIndex_Single):
    NHH_Tri = np.array([],dtype=int)
    ans = 0
    # it requires O(m)
    for pair in edgeIndex_Pair.keys():
        count = 0
        # at least one node of v is not a heavy hitter
        if dgrs[pair[0]]< math.sqrt(len(edgeIndex_Pair)) or dgrs[pair[1]]< math.sqrt(len(edgeIndex_Pair)):
            pass
        else: continue

        # if v1 < v2 (here, curved '<')
        if check_condition(pair[0],pair[1],dgrs)==1: 
            pass
        else :
            continue

        # find nodes u1,u2,...uk adjacent to v1 it requires O(sqrt(m))
        for adj in edgeIndex_Single[pair[0]]:
            if adj == pair[1]:
                continue
            else:
                a = pair[1]
                b = adj
                if check_condition(a,b,dgrs)==1:
                    vu = (a,b)
                else:
                    continue
                if vu in edgeIndex_Pair.keys():
                    count +=1
                    ans +=1
                else: continue
    return ans
    # return NHH_Tri.reshape(int(len(NHH_Tri)/3),3)
Ans2 = find_Others(input,dgrs,edgeIndex_Pair,edgeIndex_Single)
print(Ans1+Ans2)

