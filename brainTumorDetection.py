import os
import keras 
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder 
import pickle
from matplotlib.pyplot import imshow
from decouple import config

path = config('path_tumor')

encoder = OneHotEncoder()
encoder.fit([[0], [1]]) 
# 0 - Tumor
# 1 - Normal

data = []
paths = []
result = []
file_path = path + 'input/brain-mri-images-for-brain-tumor-detection/'

for r, d, f in os.walk(file_path + 'yes'):
    for file in f:
        if '.jpg' in file:
            paths.append(os.path.join(r, file))

for path in paths:
    img = Image.open(path)
    img = img.resize((128,128))
    img = np.array(img)
    if(img.shape == (128,128,3)):
        data.append(np.array(img))
        result.append(encoder.transform([[0]]).toarray())

paths = []

for r, d, f in os.walk(file_path + 'no'):
    for file in f:
        if '.jpg' in file:
            paths.append(os.path.join(r, file))

for path in paths:
    img = Image.open(path)
    img = img.resize((128,128))
    img = np.array(img)
    if(img.shape == (128,128,3)):
        data.append(np.array(img))
        result.append(encoder.transform([[1]]).toarray())

data = np.array(data)
data.shape

result = np.array(result)
result = result.reshape(3009,2)

x_train,x_test,y_train,y_test = train_test_split(data, result, test_size=0.2, shuffle=True, random_state=0)

model = Sequential()

model.add(Conv2D(32, kernel_size=(2, 2), input_shape=(128, 128, 3), padding = 'Same'))
model.add(Conv2D(32, kernel_size=(2, 2),  activation ='relu', padding = 'Same'))


model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, kernel_size = (2,2), activation ='relu', padding = 'Same'))
model.add(Conv2D(64, kernel_size = (2,2), activation ='relu', padding = 'Same'))

model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(loss = "categorical_crossentropy", optimizer='Adamax', metrics = ['accuracy'])
print(model.summary())

y_train.shape

history = model.fit(x_train, y_train, epochs = 30, batch_size = 40, verbose = 1,validation_data = (x_test, y_test))

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Test', 'Validation'], loc='upper right')
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Test', 'accuracy'],loc='upper right')
plt.show()

def names(number):
    if number==0:
        return 'Its a Tumor'
    else:
        return 'Its not a tumor'

def prediction(file_name):
    try:
        img = Image.open(file_path + file_name)
        x = np.array(img.resize((128,128)))
        x = x.reshape(1,128,128,3)
        res = model.predict_on_batch(x)
        classification = np.where(res == np.amax(res))[1][0]
        return str(res[0][classification]*100) + '% Confidence. ' + names(classification)
    except:
        return "Some error"
    #print(str(res[0][classification]*100) + '% Confidence This Is ' + names(classification))

#prediction('yes/Y6.jpg')