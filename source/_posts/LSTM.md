---
title: LSTM
date: 2019-10-22 13:31:50
categories: 其他
tags:
---

LSTM

<!--more-->

``` python

import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras import backend as K
import os
# load the dataset
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
dataframe = read_csv('xian_tianqi.csv', usecols=[1], engine='python')

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto()
config.gpu_options.allocator_type = 'BFC' #A "Best-fit with coalescing" algorithm, simplified from a version of dlmalloc.
config.gpu_options.per_process_gpu_memory_fraction = 0.8
config.gpu_options.allow_growth = True
set_session(tf.Session(config=config))

dataset = dataframe.values

# 将整型变为float
dataset = dataset.astype('float32')

look_back = 1000
print(dataset[len(dataset)-look_back:(len(dataset)), 0])
# X is the number of passengers at a given time (t) and Y is the number of passengers at the next time (t + 1).

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])

    return numpy.array(dataX), numpy.array(dataY)

# fix random seed for reproducibility
numpy.random.seed(7)
# normalize the dataset

scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)


# split into train and test sets
train_size = int(len(dataset))
train = dataset[0:train_size,:]
# use this function to prepare the train and test datasets for modeling
trainX , trainY= create_dataset(train, look_back)


def XL():
    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(128, input_shape=(look_back,1)))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')
    model.fit(trainX, trainY, epochs=40, batch_size=256, verbose=2)
    return model
ttr = trainX[trainX.shape[0]-1]
tty = []
futu = 100
with open("tqyb.honoka","w") as f:
    f.write("2019/10/18\r\n")
    for i in range(futu):
        trainX = numpy.reshape(trainX, (trainX.shape[0], look_back,1))
        if(i % look_back == 0):
            model = XL()
        ttr = numpy.reshape(ttr,(1,look_back,1))
        tty = model.predict(ttr)

        #print(trainX.shape[0],trainX.shape[1])
        ttr = ttr[0][1:look_back].reshape(look_back-1).tolist() + tty[0].tolist()

        trainX = numpy.reshape(trainX, (trainX.shape[0], look_back))
        trainX = numpy.vstack((trainX,ttr))
        #print(tty,trainY)
        trainY = numpy.reshape(trainY, (trainY.shape[0], 1))
        trainY = numpy.vstack((trainY,tty))

        print(scaler.inverse_transform(tty))
        f.write("i="+str(i) + "   " + str(scaler.inverse_transform(tty)[0][0]) + '\r\n')

#max(trainY.shape[0]-3*futu,0)
plt.plot(scaler.inverse_transform(trainY[0:trainY.shape[0]]),color="#FDA423")
plt.plot(scaler.inverse_transform(trainY[0:trainY.shape[0]-futu]),color="#808080",linestyle="--")
plt.savefig("op.png")
plt.show()

```