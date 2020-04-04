# -*- coding: utf-8 -*-
"""Caltech256Resnet50.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16Uqpi-KH7P0ud2-7HmUwMy0Ih4RKaSIx

**Downloading dataset**
"""

!wget http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar

"""**Unzipping dataset file**"""

!tar -xf 256_ObjectCategories.tar

!rm -rf '256_ObjectCategories/056.dog/greg' # remove random image folder
!rm -rf '256_ObjectCategories/198.spider/RENAME2' #remove random files

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x
from keras.preprocessing.image import ImageDataGenerator

"""**In each folder, split 30 images to training set and remaining to test set**"""

import os
import math

os.mkdir("caltech_test") # stores test data

for cat in os.listdir("256_ObjectCategories/"):
  # moves x portion of images per category into test images
  os.mkdir("caltech_test/"+cat) # new category folder
  imgs = os.listdir("256_ObjectCategories/"+cat) # all image filenames
  # split = math.floor(len(imgs)*TEST_SPLIT) 
  test_imgs = imgs[30:len(imgs)]
  for t_img in test_imgs: # move test portion
    os.rename("256_ObjectCategories/"+cat+"/"+t_img, "caltech_test/"+cat+"/"+t_img)

def fixed_generator(generator):
    for batch in generator:
        yield (batch, batch)

"""**Preparing data for feature extraction**"""

# import cv2
from keras.applications.resnet50 import preprocess_input 

train_gen_autoencoder = ImageDataGenerator(rescale=1./255) #rotation_range = 30, zoom_range = 0.20, 
# fill_mode = "nearest", shear_range = 0.20, horizontal_flip = True, 
# width_shift_range = 0.1, height_shift_range = 0.1)
train_flow = train_gen_autoencoder.flow_from_directory("256_ObjectCategories/", target_size=(256, 256), batch_size=64,class_mode=None)
valid_flow = train_gen_autoencoder.flow_from_directory("caltech_test/", target_size=(256, 256), batch_size=64,class_mode=None)

"""**Importing necessary library**"""

from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import tensorflow.keras as keras
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
import tensorflow as tf
from keras.utils import np_utils
from keras.models import load_model
from keras.datasets import cifar10
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

"""**Autoencoder model**"""

model = models.Sequential()

#encoder
# model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
# model.add(layers.MaxPooling2D((2, 2), padding='same') )
# model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
# model.add(layers.MaxPooling2D((2, 2), padding='same') )
# model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
# model.add(layers.MaxPooling2D((2, 2), padding='same') )
# model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
# model.add(layers.MaxPooling2D((2, 2), padding='same') )
model.add(layers.Conv2D(16, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPooling2D((2, 2), padding='same') )
# model.add(layers.Conv2D(8, (3, 3), activation='relu', padding='same') )
# model.add(layers.MaxPooling2D((2, 2), padding='same') )
# model.add(layers.Conv2D(8, (3, 3), activation='relu', padding='same') )
# model.add(layers.MaxPooling2D((2, 2), padding='same') )

#decoder
# model.add(layers.Conv2D(8, (3, 3), activation='relu', padding='same') )
# model.add(layers.UpSampling2D((2, 2)) )
# model.add (layers.Conv2D(8, (3, 3), activation='relu', padding='same') )
# model.add(layers.UpSampling2D((2, 2)) )
model.add(layers.Conv2D(16, (3, 3), activation='relu', padding='same'))
model.add(layers.UpSampling2D((2, 2)) )
# model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
# model.add(layers.UpSampling2D((2, 2)) )
# model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
# model.add(layers.UpSampling2D((2, 2)) )
# model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
# model.add(layers.UpSampling2D((2, 2)) )
# model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
# model.add(layers.UpSampling2D((2, 2)) )

model.add(layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same') )

model.compile(optimizer='adadelta', loss='binary_crossentropy')

"""**Training autoencoder**"""

# model.fit(training_images, training_images,
#                 epochs=5,
#                 batch_size=128,
#                 shuffle=True,
#                 validation_data=(validation_images, validation_images))
model.fit_generator(fixed_generator(train_flow), epochs=5,steps_per_epoch=7710//128, validation_steps=22897//128,validation_data = fixed_generator(valid_flow) )

"""**data augmentation and genearting data for trainig with keras flow from directory**"""

from keras.applications.resnet50 import preprocess_input # make sure to match original model's preprocessing function

# train_gen = ImageDataGenerator(validation_split=0.2, preprocessing_function=preprocess_input,rotation_range = 30, zoom_range = 0.20, 
# fill_mode = "nearest", shear_range = 0.20, horizontal_flip = True, 
# width_shift_range = 0.1, height_shift_range = 0.1)

# train_gen = ImageDataGenerator(validation_split=0.2, preprocessing_function=preprocess_input,rotation_range = 30, zoom_range = 0.20, 
# fill_mode = "nearest", shear_range = 0.20, horizontal_flip = True, 
# width_shift_range = 0.1, height_shift_range = 0.1)

train_gen = ImageDataGenerator(validation_split=0.2, preprocessing_function=preprocess_input)
train_flow = train_gen.flow_from_directory("256_ObjectCategories/", target_size=(256, 256), batch_size=128, subset="training")
valid_flow = train_gen.flow_from_directory("256_ObjectCategories/", target_size=(256, 256), batch_size=128, subset="validation")

test_gen = ImageDataGenerator(preprocessing_function=preprocess_input)
test_flow = test_gen.flow_from_directory("caltech_test", target_size=(256, 256), batch_size=32)

"""**Preparing model with the help of resnet 50 pretrained model on imagenet**"""

from keras.applications.resnet50 import ResNet50
from keras.layers import GlobalAveragePooling2D, BatchNormalization, Dropout, Dense
from keras.models import Model


res = ResNet50(weights='imagenet', include_top=False, input_shape=(256, 256, 3)) # load resnet model, with pretrained imagenet weights.

for layer in res.layers: # because our finetuning dataset is similar to the imagenet dataset, we can freeze the convolutional layers
  layer.trainable = False

x = res.output # get the output from the loaded model
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)
x = Dense(257, activation='softmax')(x)

model = Model(res.input, x) # create the model, setting input/output

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy']) # compile the model - we're training using the Adam Optimizer and Categorical Cross Entropy as the loss function


model.summary() # prints the structure of our model

"""**Training model**"""

import time
start = time.time()
history = model.fit_generator(train_flow, epochs=15, validation_data=valid_flow) 
end = time.time()

print("Total Training time: ",(end-start))

import keras
from matplotlib import pyplot as plt

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
plt.savefig("performance_caltech256.png")

"""**Evaluating model**"""

score = model.evaluate(test_flow)

print('The model achieved a accuracy of %.2f%%.' % (score[1]*100))