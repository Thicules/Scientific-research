from keras.models import Sequential
from keras.layers import Conv2D,Activation,MaxPooling2D,Dense,Flatten,Dropout
import numpy as np
classifier = Sequential()
classifier.add(Conv2D(32,(3,3),input_shape=(64,64,3)))
classifier.add(Activation('relu'))
classifier.add(MaxPooling2D(pool_size =(2,2)))
classifier.add(Flatten())
classifier.add(Dense(64))
classifier.add(Activation('relu'))
classifier.add(Dropout(0.5))
classifier.add(Dense(1))
classifier.add(Activation('sigmoid'))
classifier.summary()
classifier.compile(optimizer ='rmsprop',
                   loss ='binary_crossentropy',
                   metrics =['accuracy'])
classifier.compile(optimizer ='rmsprop',
                   loss ='binary_crossentropy',
                   metrics =['accuracy'])
from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale =1./255,
                                   shear_range =0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip =True)
test_datagen = ImageDataGenerator(rescale = 1./255)
training_set = train_datagen.flow_from_directory('/content/drive/MyDrive/NCKH/Roads/train_road',
                                                 target_size=(64,64),
                                                 batch_size= 32,
                                                 class_mode='binary')

test_set = test_datagen.flow_from_directory('/content/drive/MyDrive/NCKH/Roads/validation_road',
                                            target_size = (64,64),
                                           batch_size = 32,
                                           class_mode ='binary')
from IPython.display import display
from PIL import Image
classifier.fit_generator(training_set,
                         steps_per_epoch =945,
                         epochs = 15,
                         validation_data =test_set,
                         validation_steps = 8161)
classifier.save('road_cnn_model.h5')