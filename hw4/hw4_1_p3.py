import sys
import csv
import math
import numpy as np

def sigmoid(x):
    return 1/(1 + math.exp(-x))
apply_Sigmoid = np.vectorize(sigmoid)

def calculate_MSE(y,y_hat):
    return np.square(y-y_hat).sum()/len(y)

# Output to Labeled_Output
def OneHot_encode(Output):
    idx_Arr = np.array([],dtype=int)
    for vec in Output:
        idx_Arr = np.append(idx_Arr,np.argmax(vec))

    Labeled_Output = np.array([],dtype=int)
    for i in range(len(idx_Arr)):
        a = np.zeros(10)
        a[idx_Arr[i]] = 1
        Labeled_Output = np.append(Labeled_Output,a)
    Labeled_Output = Labeled_Output.reshape(1000,10)
    return Labeled_Output

training = sys.argv[1]
testing = sys.argv[2]
train_data, train_label = np.array([]),np.array([])
test_data, test_label = np.array([]),np.array([])

# Make train_data, train_label
f = open(training,'r')
while True:
    line = f.readline()
    if not line:
        break
    vec = line.split(',')
    # 784 Features to np array
    arr = np.array([],dtype= float)
    aList = vec[0:-1]
    for num in aList:
        arr=np.append(arr, float(num))
    # Label one hot encoding
    label = int(float(vec[-1].strip()))
    one_hot_encode = np.zeros(10)
    one_hot_encode[label] = 1
    train_data = np.append(train_data, arr)
    train_label = np.append(train_label, one_hot_encode)
f.close()
train_data = train_data.reshape(1000,784)
train_label = train_label.reshape(1000,10)

# Make train_data, train_label
f = open(testing,'r')
while True:
    line = f.readline()
    if not line:
        break
    vec = line.split(',')
    # 784 Features to np array
    arr = np.array([],dtype= float)
    aList = vec[0:-1]
    for num in aList:
        arr=np.append(arr, float(num))
    # Label one hot encoding
    label = int(float(vec[-1].strip()))
    one_hot_encode = np.zeros(10)
    one_hot_encode[label] = 1
    test_data = np.append(test_data, arr)
    test_label = np.append(test_label, one_hot_encode)
f.close()
test_data = test_data.reshape(1000,784)
test_label = test_label.reshape(1000,10)


class Fully_Connected_Layer:
    def __init__(self, learning_rate):
        self.InputDim = 784
        self.HiddenDim = 128
        self.OutputDim = 10
        self.learning_rate = learning_rate
        
        '''Weight Initialization'''
        # Gauissian normalization
        self.W1 = np.random.randn(self.InputDim, self.HiddenDim) # W1(784 x 128)
        self.W2 = np.random.randn(self.HiddenDim, self.OutputDim) # W2(128 x 10)
        
    def Forward(self, Input):
        '''Implement forward propagation'''
        # input(1000 x 784), self.W1(784 x 128) = 1000 x 128 
        hidden_Layer = apply_Sigmoid(np.matmul(Input,self.W1)) 
        Output = apply_Sigmoid(np.matmul(hidden_Layer,self.W2)) # Output(1000 x 10)
        return Output

### Whole process of Forward: 
### X ->weight->U->sigmoid->V  ->weight->Z->sigmoid->O 

    def Backward(self, Input, Label, Output):
        '''Implement backward propagation'''
        # Gradient descent for W2
        dLdo = (2.0/10)*(Output - Label) # (1000 x 10)
        dodz = Output*(1-Output) # (1000 x 10)
        dzdw2 = apply_Sigmoid(np.matmul(Input,self.W1)) # (1000 x 128)
        dLdw2 = np.matmul((dzdw2.T),dodz*dLdo) # there are 128 x 10 weights

        dLdv = np.matmul(dodz*dLdo,(self.W2).T) # (1000 x 10)*(128 x 10).T -> (1000 x 128)
        v = apply_Sigmoid(np.matmul(Input,self.W1)) # (1000 x 128)
        dvdu = v*(1-v) # (1000 x 128)
        dudw1 = Input # (1000 x 748)

        dLdw1 = np.matmul(dudw1.T,dLdv*dvdu) # -> there are 784 x 128 weights

        '''Update parameters using gradient descent'''
        self.W2 = self.W2 - self.learning_rate*(dLdw2)
        self.W1 = self.W1 - self.learning_rate*(dLdw1)

        return

    def Train(self, Input, Label):
        Output = self.Forward(Input)
        self.Backward(Input, Label, Output)     

'''Construct a fully-connected network'''
eta = 0.01      
Network = Fully_Connected_Layer(eta)

'''Train the network for the number of iterations'''
'''Implement function to measure the accuracy'''

iterations = 5000
for i in range(iterations):
    Network.Train(train_data, train_label)

o = Network.Forward(train_data)

def calculate_Acc(o,train_label):
    count = 0
    for i in range(len(o)):
        if np.array_equal(OneHot_encode(o)[i],train_label[i]):
            count+=1
    return count/1000.0

print(calculate_Acc(o,train_label))

test_o = apply_Sigmoid(
    np.matmul(
        apply_Sigmoid(np.matmul(test_data,Network.W1)),Network.W2
    )
)
print(calculate_Acc(test_o,test_label))
print(iterations)
print(eta)