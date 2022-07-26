#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 21:16:16 2022

@author: kbelbase
"""
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import matplotlib.pyplot as plt


def preprocess_Image(Image):
    #First load the image and convert to the same size as train image
    image = load_img(Image,grayscale=True,target_size=(28,28))                    
    #Convert the image data to an array 
    image = img_to_array(image)
    #Reshape an image to have the same shape as the trained image
    image = image.reshape(1,28,28,1)    
    #Convert integer value of pixel to floating value
    image = image.astype('float32')
    #Rescale pixels value 0 to 255 into 0 to 1
    image = image/255.0
    #Pass the final image if this function is invoked
    return image    

def predictOn_new_image():
    #Load an image by passing the location
    answer     = input('Given a name or the path for example image\n')
    if len(answer) > 0:
        image  = preprocess_Image(answer)
    else:
        image      =  preprocess_Image('Digit_Images/sample_image.png')
    #Load the already trained image
    model      = load_model('2022_July_Sunday_03_07_07.h5')    
    #Predict the class of image 
    prediction = model.predict(image)
    #We used softmax activation function in our final layer as a result 
    #prediction is made in terms of probability. Consequently all ten classes 
    #have none -zero value and we take maximum value from this array.
    final_predict = np.argmax(prediction)
    #Again reshape back to three dimensional array to plot
    image = image.reshape(28,28,1)
    #imshow of plt is used to display array to image
    plt.imshow(image)    
    print(f'The model sees the number {final_predict} in the uploaded image.')
    print(f'How right I am :-)')
    
    
if __name__=='__main__':
    predictOn_new_image()            

