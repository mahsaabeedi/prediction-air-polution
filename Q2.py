# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19VHs6Su_XUfVQHgIcm4TokH4K1iyC557
"""

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
import time
from math import sqrt
from sklearn.preprocessing import MinMaxScaler
import numpy.ma as ma
from sklearn import metrics

n = 12000
file = np.load('polution_dataSet.npy')


train_data= file[:12000,:]
test_data=file[12000:15000,:]

########mising data
missingdata=np.copy(train_data)

for j in range (8):
    index = np.random.choice( 12000, 2400, replace=False)
    for i in range(2400):
        missingdata[index[i]][j]=np.nan

print('number of nan data in each column:',np.count_nonzero(np.isnan(missingdata), axis=0))
print('data shape:' ,missingdata.shape)
print('\n changed column:\n',missingdata[20],'\noriginal column\n',train_data[20])
print('changed column:\n',missingdata[110],'\noriginal column\n',train_data[110])

##mask with 0
masked0 = np.where(np.isnan(missingdata), 0, missingdata)

###################comput MSE
mseZERO=np.zeros(8)
for i in range(8):
  mseZERO[i]=metrics.mean_squared_error(train_data[:,i], masked0[:,i])*5

print('mseZERO :',mseZERO)

#############mask whit mean

#model.add(Masking(mask_value=0., input_shape=(timesteps, features)))

masked=np.where(np.isnan(missingdata), ma.array(missingdata, mask=np.isnan(missingdata)).mean(axis=0), missingdata) 

###################comput MSE
mseMEAN=np.zeros(8)
for i in range(8):
  mseMEAN[i]=metrics.mean_squared_error(train_data[:,i], masked[:,i])*5

print('mse (mean):',mseMEAN)

#######1000 nearst neighbor
from sklearn.impute import KNNImputer
X = np.copy(missingdata)
imputer = KNNImputer(n_neighbors=1000, weights="uniform")
X=imputer.fit_transform(X)

mseKNN=np.zeros(8)
for i in range(8):
  mseKNN[i]=metrics.mean_squared_error(train_data[:,i], X[:,i])*5

print('mse (KNN):',mseKNN)

#examples of imputation 
print('original column\n',train_data[20])
print('\n changed column:\n',missingdata[20])
print('\n zero mask :\n',masked0[20])
print('\n mean imputation :\n',masked[20])
print('\n KNN imputation :\n',X[20])

#####################LSTM-masked data
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
import time
from math import sqrt
from sklearn.preprocessing import MinMaxScaler


n = 12000
file = np.load('polution_dataSet.npy')

a1 = X[:,0:8]
a2 = X[:,0]
b1 = np.zeros((11,8))


train = 9000-11
valid = 3000-11

X_Valid = np.zeros((valid+1,11,8))
Y_Valid = np.zeros((valid+1,1))

X_Train = np.zeros((train+1,11,8))
Y_Train = np.zeros((train+1,1))

for i in range(train+1):
    for j in range(11):
        b1[j] = a1[j + i]
    X_Train[i] = b1
    Y_Train[i] = a2[11 + i]


for  i in range(valid ):
        iddx = i + 9000
        for j in range(11):
            b1[j] = a1[j+iddx]
        X_Valid[i] = b1
        Y_Valid[i] = a2[11 + iddx]

a1 = file[:,0:8]
a2 = file[:,0]
b1 = np.zeros((11,8))

X_Test = np.zeros((int(3000/12),11,8))
Y_Test = np.zeros((int(3000/12),1))
for  i in range(int(3000/12)):
    idx = 12000 + i*12
    for j in range(11):
        b1[j] = a1[j + idx]

    X_Test[i] = b1
    Y_Test[i] = a2[11 + idx]

print(Y_Test[int(3000/12)-1])
print(file[int(3000/12)-1])



start = time.time()


model = Sequential()
model.add(LSTM(32,input_shape=(11,8),return_sequences=False, dropout=0.1, recurrent_dropout=0.1))
#model.add(Dropout(0.1))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
print(model.summary())
history = model.fit(X_Train, Y_Train, validation_data=(X_Valid, Y_Valid),verbose=2, epochs=100)

# Final evaluation of the model
scores = model.evaluate(X_Test, Y_Test, verbose=0)


print("Accuracy: %.2f%%" % (scores[1]*100))

done = time.time()
elapsed = done - start
print("Time of execution:   ",elapsed)

training_loss = history.history['loss']
test_loss = history.history['val_loss']
epoch_count = range(1, len(training_loss)+1)
pyplot.plot(epoch_count, training_loss)
pyplot.plot(epoch_count, test_loss)
pyplot.ylabel('Loss')
pyplot.xlabel('Epochs')
pyplot.legend(['Train', 'Test'], loc='upper right')
pyplot.show()

training_acc = history.history['accuracy']
test_acc = history.history['val_accuracy']
epoch_count = range(1, len(training_acc)+1)
pyplot.plot(epoch_count, training_acc)
pyplot.plot(epoch_count, test_acc)
pyplot.ylabel('Accuracy')
pyplot.xlabel('Epochs')
pyplot.legend(['Train', 'Test'], loc='upper right')
pyplot.show()


out1 = np.zeros(n)
out2 = np.zeros(n)


trainPredict = model.predict(X_Test)



fig, ax = pyplot.subplots(figsize=(17,8))
ax.set_title('Prediction vs. Actual after 100 epochs of training')
ax.plot(Y_Test[:,], label='True Data', color='green', linewidth='3')
ax.plot(trainPredict[:,], label='Prediction', color='red', linewidth='2')
pyplot.legend()
pyplot.show()

fig, ax = pyplot.subplots(figsize=(10,10))
ax.set_title('Prediction vs. Actual after 100 epochs of training')
xx=np.arange(2)*0.45
ax.plot(xx,xx)
ax.scatter(trainPredict[:,],Y_Test[:,])
pyplot.legend()
pyplot.show()

#####################LSTM-original data
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
import time
from math import sqrt
from sklearn.preprocessing import MinMaxScaler


n = 12000
file = np.load('polution_dataSet.npy')

a1 = file[:,0:8]
a2 = file[:,0]
b1 = np.zeros((11,8))


train = 9000-11
valid = 3000-11

X_Valid = np.zeros((valid+1,11,8))
Y_Valid = np.zeros((valid+1,1))

X_Train = np.zeros((train+1,11,8))
Y_Train = np.zeros((train+1,1))

for i in range(train+1):
    for j in range(11):
        b1[j] = a1[j + i]
    X_Train[i] = b1
    Y_Train[i] = a2[11 + i]


for  i in range(valid ):
        iddx = i + 9000
        for j in range(11):
            b1[j] = a1[j+iddx]
        X_Valid[i] = b1
        Y_Valid[i] = a2[11 + iddx]

a1 = file[:,0:8]
a2 = file[:,0]
b1 = np.zeros((11,8))

X_Test = np.zeros((int(3000/12),11,8))
Y_Test = np.zeros((int(3000/12),1))
for  i in range(int(3000/12)):
    idx = 12000 + i*12
    for j in range(11):
        b1[j] = a1[j + idx]

    X_Test[i] = b1
    Y_Test[i] = a2[11 + idx]

print(Y_Test[int(3000/12)-1])
print(file[int(3000/12)-1])



start = time.time()


model = Sequential()
model.add(LSTM(32,input_shape=(11,8),return_sequences=False, dropout=0.1, recurrent_dropout=0.1))
#model.add(Dropout(0.1))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
print(model.summary())
history = model.fit(X_Train, Y_Train, validation_data=(X_Valid, Y_Valid),verbose=2, epochs=100)

# Final evaluation of the model
scores = model.evaluate(X_Test, Y_Test, verbose=0)


print("Accuracy: %.2f%%" % (scores[1]*100))

done = time.time()
elapsed = done - start
print("Time of execution:   ",elapsed)

training_loss = history.history['loss']
test_loss = history.history['val_loss']
epoch_count = range(1, len(training_loss)+1)
pyplot.plot(epoch_count, training_loss)
pyplot.plot(epoch_count, test_loss)
pyplot.ylabel('Loss')
pyplot.xlabel('Epochs')
pyplot.legend(['Train', 'Test'], loc='upper right')
pyplot.show()

training_acc = history.history['accuracy']
test_acc = history.history['val_accuracy']
epoch_count = range(1, len(training_acc)+1)
pyplot.plot(epoch_count, training_acc)
pyplot.plot(epoch_count, test_acc)
pyplot.ylabel('Accuracy')
pyplot.xlabel('Epochs')
pyplot.legend(['Train', 'Test'], loc='upper right')
pyplot.show()


out1 = np.zeros(n)
out2 = np.zeros(n)


trainPredict = model.predict(X_Test)



fig, ax = pyplot.subplots(figsize=(17,8))
ax.set_title('Prediction vs. Actual after 100 epochs of training')
ax.plot(Y_Test[:,], label='True Data', color='green', linewidth='3')
ax.plot(trainPredict[:,], label='Prediction', color='red', linewidth='2')
pyplot.legend()
pyplot.show()

fig, ax = pyplot.subplots(figsize=(10,10))
ax.set_title('Prediction vs. Actual after 100 epochs of training')
xx=np.arange(2)*0.45
ax.plot(xx,xx)
ax.scatter(trainPredict[:,],Y_Test[:,])
pyplot.legend()
pyplot.show()

#####################GRU-masked data
from math import sqrt

import numpy as np
from keras.layers import Dense, Dropout
from keras.layers import GRU
from keras.models import Sequential
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
import time
import math

n = 12000
file = np.load('polution_dataSet.npy')

a1 = X[:,0:8]
a2 = X[:,0]
b1 = np.zeros((11,8))


train = 9000-11
valid = 3000-11

X_Valid = np.zeros((valid+1,11,8))
Y_Valid = np.zeros((valid+1,1))

X_Train = np.zeros((train+1,11,8))
Y_Train = np.zeros((train+1,1))

for i in range(train+1):
    for j in range(11):
        b1[j] = a1[j + i]
    X_Train[i] = b1
    Y_Train[i] = a2[11 + i]


for  i in range(valid ):
        iddx = i + 9000
        for j in range(11):
            b1[j] = a1[j+iddx]
        X_Valid[i] = b1
        Y_Valid[i] = a2[11 + iddx]

a1 = file[:,0:8]
a2 = file[:,0]
b1 = np.zeros((11,8))

X_Test = np.zeros((int(3000/12),11,8))
Y_Test = np.zeros((int(3000/12),1))
for  i in range(int(3000/12)):
    idx = 12000 + i*12
    for j in range(11):
        b1[j] = a1[j + idx]

    X_Test[i] = b1
    Y_Test[i] = a2[11 + idx]

print(Y_Test[int(3000/12)-1])
print(file[int(3000/12)-1])



start = time.time()


model = Sequential()
model.add(GRU(32,input_shape=(11,8), return_sequences=False,activation='tanh'))
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])#mean_squared_error   adam   RMSprop    loss mae
print(model.summary())
history = model.fit(X_Train, Y_Train,validation_data=(X_Valid, Y_Valid),verbose=2, epochs=100, shuffle=False)

# Final evaluation of the model
scores = model.evaluate(X_Test, Y_Test, verbose=0)


print("Accuracy: %.2f%%" % (scores[1]*100))

done = time.time()
elapsed = done - start
print("Time of execution:   ",elapsed)

training_loss = history.history['loss']
test_loss = history.history['val_loss']
epoch_count = range(1, len(training_loss)+1)
pyplot.plot(epoch_count, training_loss)
pyplot.plot(epoch_count, test_loss)
pyplot.ylabel('Loss')
pyplot.xlabel('Epochs')
pyplot.legend(['Train', 'Test'], loc='upper right')
pyplot.show()

training_acc = history.history['accuracy']
test_acc = history.history['val_accuracy']
epoch_count = range(1, len(training_acc)+1)
pyplot.plot(epoch_count, training_acc)
pyplot.plot(epoch_count, test_acc)
pyplot.ylabel('Accuracy')
pyplot.xlabel('Epochs')
pyplot.legend(['Train', 'Test'], loc='upper right')
pyplot.show()


out1 = np.zeros(n)
out2 = np.zeros(n)


trainPredict = model.predict(X_Test)



fig, ax = pyplot.subplots(figsize=(17,8))
ax.set_title('Prediction vs. Actual after 100 epochs of training')
ax.plot(Y_Test[:,], label='True Data', color='green', linewidth='3')
ax.plot(trainPredict[:,], label='Prediction', color='red', linewidth='2')
pyplot.legend()
pyplot.show()

fig, ax = pyplot.subplots(figsize=(10,10))
ax.set_title('Prediction vs. Actual after 100 epochs of training')
xx=np.arange(2)*0.45
ax.plot(xx,xx)
ax.scatter(trainPredict[:,],Y_Test[:,])
pyplot.legend()
pyplot.show()

#####################GRU-original data
from math import sqrt

import numpy as np
from keras.layers import Dense, Dropout
from keras.layers import GRU
from keras.models import Sequential
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
import time
import math

n = 12000
file = np.load('polution_dataSet.npy')

a1 = file[:,0:8]
a2 = file[:,0]
b1 = np.zeros((11,8))


train = 9000-11
valid = 3000-11

X_Valid = np.zeros((valid+1,11,8))
Y_Valid = np.zeros((valid+1,1))

X_Train = np.zeros((train+1,11,8))
Y_Train = np.zeros((train+1,1))

for i in range(train+1):
    for j in range(11):
        b1[j] = a1[j + i]
    X_Train[i] = b1
    Y_Train[i] = a2[11 + i]


for  i in range(valid ):
        iddx = i + 9000
        for j in range(11):
            b1[j] = a1[j+iddx]
        X_Valid[i] = b1
        Y_Valid[i] = a2[11 + iddx]

a1 = file[:,0:8]
a2 = file[:,0]
b1 = np.zeros((11,8))

X_Test = np.zeros((int(3000/12),11,8))
Y_Test = np.zeros((int(3000/12),1))
for  i in range(int(3000/12)):
    idx = 12000 + i*12
    for j in range(11):
        b1[j] = a1[j + idx]

    X_Test[i] = b1
    Y_Test[i] = a2[11 + idx]

print(Y_Test[int(3000/12)-1])
print(file[int(3000/12)-1])



start = time.time()


model = Sequential()
model.add(GRU(32,input_shape=(11,8), return_sequences=False,activation='tanh'))
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])#mean_squared_error   adam   RMSprop    loss mae
print(model.summary())
history = model.fit(X_Train, Y_Train,validation_data=(X_Valid, Y_Valid),verbose=2, epochs=100, shuffle=False)

# Final evaluation of the model
scores = model.evaluate(X_Test, Y_Test, verbose=0)


print("Accuracy: %.2f%%" % (scores[1]*100))

done = time.time()
elapsed = done - start
print("Time of execution:   ",elapsed)

training_loss = history.history['loss']
test_loss = history.history['val_loss']
epoch_count = range(1, len(training_loss)+1)
pyplot.plot(epoch_count, training_loss)
pyplot.plot(epoch_count, test_loss)
pyplot.ylabel('Loss')
pyplot.xlabel('Epochs')
pyplot.legend(['Train', 'Test'], loc='upper right')
pyplot.show()

training_acc = history.history['accuracy']
test_acc = history.history['val_accuracy']
epoch_count = range(1, len(training_acc)+1)
pyplot.plot(epoch_count, training_acc)
pyplot.plot(epoch_count, test_acc)
pyplot.ylabel('Accuracy')
pyplot.xlabel('Epochs')
pyplot.legend(['Train', 'Test'], loc='upper right')
pyplot.show()


out1 = np.zeros(n)
out2 = np.zeros(n)


trainPredict = model.predict(X_Test)



fig, ax = pyplot.subplots(figsize=(17,8))
ax.set_title('Prediction vs. Actual after 100 epochs of training')
ax.plot(Y_Test[:,], label='True Data', color='green', linewidth='3')
ax.plot(trainPredict[:,], label='Prediction', color='red', linewidth='2')
pyplot.legend()
pyplot.show()

fig, ax = pyplot.subplots(figsize=(10,10))
ax.set_title('Prediction vs. Actual after 100 epochs of training')
xx=np.arange(2)*0.45
ax.plot(xx,xx)
ax.scatter(trainPredict[:,],Y_Test[:,])
pyplot.legend()
pyplot.show()

