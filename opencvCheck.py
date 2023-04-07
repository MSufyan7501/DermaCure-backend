
import cv2
import tensorflow as tf
import os
# from google.colab.patches import cv2_imshow
fname="rn_image_picker_lib_temp_ab74c2e3-9d05-4fc5-8c8b-e897405bc7ae.jpg"
originalImg=cv2.imread(os.path.join("static","uploads",fname))
greyScaleImg=cv2.imread(os.path.join("static","uploads",fname),0)
originalImg=cv2.resize(originalImg, (200,200), interpolation = cv2.INTER_AREA)
greyScaleImg=cv2.resize(greyScaleImg, (200,200), interpolation = cv2.INTER_AREA)

filterSize = (17,17)
kernel = cv2.getStructuringElement(1,filterSize)

blackhat = cv2.morphologyEx(greyScaleImg, cv2.MORPH_BLACKHAT, kernel)
ret, thresh2 = cv2.threshold(blackhat,10,255,cv2.THRESH_BINARY)

dst = cv2.inpaint(originalImg,thresh2,1,cv2.INPAINT_TELEA)

cv2.imwrite("/content/abcd.jpg",dst,[int(cv2.IMWRITE_JPEG_QUALITY), 90])


cv2.imwrite(os.path.join("static","uploads",'image.jpg'),dst,[int(cv2.IMWRITE_JPEG_QUALITY), 90])
filterimage=cv2.imread(os.path.join("static","uploads","image.jpg"))

cv2.imshow('origional image',originalImg)
cv2.imshow('cleared image',filterimage)

cv2.waitKey(0)