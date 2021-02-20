#!/usr/bin/env python
# coding: utf-8

# In[44]:


import cv2
import numpy as np

##################  1st TASK  #################

img1 = cv2.imread("moon-photography-camera.jpg") # reads the image

image_1 = cv2.rectangle(img1, (75,90), (200, 300), (0,0,255), 3)       # draws a rectangle in img1 with start at (75,90), end at (200,300), red colored line with thickness 3
image_1 = cv2.rectangle(image_1, (395, 125), (430, 160), (0, 0, 0), 1) # draws a rectangle in imgage_1 with start at (395, 125), end at (430, 160), black colored line with thickness 1

cv2.imwrite('image_1.jpg', image_1) # saves result as image_1.jpg
cv2.imshow('image_1', image_1)      # shows the result

###############################################
##################  2nd TASK  #################

img2 = cv2.imread("moon-photography-camera.jpg") # reads the image

image_2_1 = img2[90:300, 75:200]   # cuts the region of interest - [x1:x2, y1:y2]
image_2_2 = img2[125:160, 395:430] # 

cv2.imshow('image_2_1', image_2_1) # shows the result
cv2.imshow('image_2_2', image_2_2) # 

cv2.imwrite('image_2_1.jpg', image_2_1) # saves result as image_2_1.jpg
cv2.imwrite('image_2_2.jpg', image_2_2) # saves result as image_2_2.jpg

###############################################
##################  3rd TASK  #################

img3 = cv2.imread("flower.jpg") # reads the image

h, w, d = img.shape                           # takes height, width and depth of the image
img3 = cv2.resize(img3, (int(w/4), int(h/4))) # resizes the image, 4 times smaller

kernel_5x5 = np.ones((5,5), np.float32) / 25 # matrix of kernel to filter the image by 2D convolution 
blurred = cv2.filter2D(img3, -1, kernel_5x5) # filtering to blur

kernel_3x3 = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) # matrix of kernel to filter the image by 2D convolution
sharpened = cv2.filter2D(img3, -1, kernel_3x3)             # filtering to sharpen

cv2.imshow('resized original', img3) # shows the original image in resized form
cv2.imshow('blurred', blurred)       # shows the result
cv2.imshow('sharpened', sharpened)   #

cv2.imwrite('image_3_1.jpg', blurred)   # saves result as image_3_1.jpg
cv2.imwrite('image_3_2.jpg', sharpened) # saves result as image_3_2.jpg

###############################################
##################  4th TASK  #################

img4 = cv2.imread("dark.jpg") # reads the image

gray = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY) # converts the image to grayscale 
equalized = cv2.equalizeHist(gray)            # uses histogram equalization to increase the brightness

cv2.imshow('original', img4)       # shows the original image
cv2.imshow('equalized', equalized) # shows the result

cv2.imwrite('image_4.jpg', equalized) # saves result as image_4.jpg

cv2.waitKey(0) # displays the window infinitely until any keypress

