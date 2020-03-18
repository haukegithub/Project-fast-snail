#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras.applications.vgg16 import VGG16
from keras.optimizers import Adam

def labels_to_y_train(labels):
	new_labels = []
	for label in labels:
		if label == 1: new_label = 0
		if label == 2: new_label = 1
		if label == 3: new_label = 2
		if label == 4: new_label = 3
		new_labels.append(new_label)
	return np_utils.to_categorical(new_labels, 4)

# Laden der Daten
tr_data = np.load('./train_images.npz')
x_train = tr_data['data']
tr_labels = tr_data['labels']
y_train = labels_to_y_train(tr_labels)

va_data = np.load('./val_images.npz')
x_val = va_data['data']
vl_labels = va_data['labels']
y_val = labels_to_y_train(vl_labels)

# Erstellen des Models
vgg16_model = VGG16()

# Uebersetzen zu sequential
model = Sequential()
for layer in vgg16_model.layers:
	model.add(layer)

# Austauschen der 1000 outputlayer mit 4 
model.layers.pop()

for layer in model.layers:
	layer.trainable = False

model.add(Dense(4, activation='softmax'))

model.summary()

model.compile(Adam(lr=.0001), loss='categorical_crossentropy', metrics=['accuracy'])

train_data = (x_train, y_train)
val_data = (x_val, y_val)
model.fit_generator(train_data, steps_per_epoch=4, validation_data=val_data, validation_steps=4, epochs=5, verbose=2)


model.summary()
