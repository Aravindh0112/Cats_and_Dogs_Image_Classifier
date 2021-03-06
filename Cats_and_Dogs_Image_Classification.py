# -*- coding: utf-8 -*-
"""ANN(Dogs_and_Cats).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OZZEfKX11JLjCgMH2vrexRQamtlc5xGn
"""

import os
import zipfile
import random
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from shutil import copyfile

!wget --no-check-certificate \
    "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip" \
    -O "/tmp/cats-and-dogs.zip"

local_zip = '/tmp/cats-and-dogs.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()
#downloading the dataset and saving them in a temporary directory.

print(len(os.listdir('/tmp/PetImages/Cat/')))
print(len(os.listdir('/tmp/PetImages/Dog/')))
#printing out the length of the individual directories.

# Use os.mkdir to create your directories
# You will need a directory for cats-v-dogs, and subdirectories for training
# and testing. These in turn will need subdirectories for 'cats' and 'dogs'
to_create = [
    '/tmp/cats-v-dogs',
    '/tmp/cats-v-dogs/training',
    '/tmp/cats-v-dogs/testing',
    '/tmp/cats-v-dogs/training/cats',
    '/tmp/cats-v-dogs/training/dogs',
    '/tmp/cats-v-dogs/testing/cats',
    '/tmp/cats-v-dogs/testing/dogs'
]

for directory in to_create:
    try:
        os.mkdir(directory)
        print(directory, 'created')
    except:
        print(directory, 'failed')

def split_data(SOURCE,TRAINING,TESTING,Split_size):
  all_files=[]
  for file_name in os.listdir(SOURCE):
    file_path= SOURCE + file_name

    if os.path.getsize(file_path):
      all_files.append(file_name)
      
    else:
      print('{} is of zero size, so ignoring'.format(file_name))

  n_files=len(all_files)
  split_point=int(n_files*Split_size)

  shuffled= random.sample(all_files,n_files)
  train_set=shuffled[:split_point]
  test_set=shuffled[split_point:]

  for file_name in train_set:
    copyfile(SOURCE + file_name,TRAINING + file_name)
  for file_name in test_set:
    copyfile(SOURCE + file_name,TESTING + file_name)

CAT_SOURCE= "/tmp/PetImages/Cat/"
CAT_TRAIN_DIR="/tmp/cats-v-dogs/training/cats/"
CAT_TEST_DIR="/tmp/cats-v-dogs/testing/cats/"
DOG_TRAIN_DIR="/tmp/cats-v-dogs/training/dogs/"
DOG_SOURCE ="/tmp/PetImages/Dog/"
DOG_TEST_DIR="/tmp/cats-v-dogs/testing/dogs/"
split_size=0.9
split_data(CAT_SOURCE,CAT_TRAIN_DIR,CAT_TEST_DIR,split_size)
split_data(DOG_SOURCE,DOG_TRAIN_DIR,DOG_TEST_DIR,split_size)

print(len(os.listdir('/tmp/cats-v-dogs/training/cats/')))
print(len(os.listdir('/tmp/cats-v-dogs/training/dogs/')))
print(len(os.listdir('/tmp/cats-v-dogs/testing/cats/')))
print(len(os.listdir('/tmp/cats-v-dogs/testing/dogs/')))

model=tf.keras.Sequential([
       tf.keras.layers.Conv2D(16,(3,3),input_shape=(150,150,3),activation='relu'),
       tf.keras.layers.MaxPooling2D(2,2),
       tf.keras.layers.Conv2D(32,(3,3),activation='relu'),
       tf.keras.layers.MaxPooling2D(2,2),
       tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
       tf.keras.layers.MaxPooling2D(2,2),
       #tf.keras.layers.Conv2D(256,(3,3),activation='relu'),
       #tf.keras.layers.MaxPooling2D(2,2),

       tf.keras.layers.Flatten(),
       tf.keras.layers.Dense(512,activation='relu'),
       #tf.keras.layers.Dense(128,activation='relu'),
       tf.keras.layers.Dense(1,activation='sigmoid')
])

model.summary()

model.compile(optimizer=RMSprop(lr=0.001),loss='binary_crossentropy',metrics=['accuracy'])

TRAINING_DIR='/tmp/cats-v-dogs/training'
train_datagen=ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    shear_range=0.2,
    fill_mode='nearest',
    horizontal_flip=True
)
train_generator=train_datagen.flow_from_directory(
    TRAINING_DIR,
    batch_size=100,
       class_mode='binary',
    target_size=(150,150)
)

VALID_DIR='/tmp/cats-v-dogs/testing'
valid_datagen=ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
valid_generator=valid_datagen.flow_from_directory(
    VALID_DIR,
    target_size=(150,150),
    batch_size=100,
    class_mode='binary'
)

history=model.fit_generator(
    train_generator,
    epochs=15,
    #steps_per_epoch=8,
    verbose=1,
    validation_data=valid_generator)

# Commented out IPython magic to ensure Python compatibility.
# PLOT LOSS AND ACCURACY
# %matplotlib inline

import matplotlib.image  as mpimg
import matplotlib.pyplot as plt

#-----------------------------------------------------------
# Retrieve a list of list results on training and test data
# sets for each training epoch
#-----------------------------------------------------------
acc=history.history['accuracy']
val_acc=history.history['val_accuracy']
loss=history.history['loss']
val_loss=history.history['val_loss']

epochs=range(len(acc)) # Get number of epochs

#------------------------------------------------
# Plot training and validation accuracy per epoch
#------------------------------------------------
#-----------------------------------------------
plt.plot(epochs, acc, 'r', "Training Accuracy")
plt.plot(epochs, val_acc, 'b', "Validation Accuracy")
plt.title('Training and validation accuracy')
plt.figure()

#------------------------------------------------
# Plot training and validation loss per epoch
#------------------------------------------------
#------------------------------------------------
plt.plot(epochs, loss, 'r', "Training Loss")
plt.plot(epochs, val_loss, 'b', "Validation Loss")


plt.title('Training and validation loss')

# Desired output. Charts with training and validation metrics. No crash :),happy coding!!!!!

import numpy as np
from google.colab import files
from keras.preprocessing import image

uploaded = files.upload()

for fn in uploaded.keys():
 
  # predicting images
  path = '/content/' + fn
  img = image.load_img(path, target_size=(150,150))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)
  print(classes[0])
  if classes[0]>0.5:
    print(fn + " is a dog")
  else:
    print(fn + " is a cat")