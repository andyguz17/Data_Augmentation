import numpy as np
import cv2 

def HorizontalFlip(img,bbox):	
	himg = cv2.flip(img, 1)
	bbx = np.copy(bbox)
	for i in range(bbox.shape[1]):
		bbx[0,i] = img.shape[1]-bbox[2,i]
		bbx[2,i] = (bbox[2,i]-bbox[0,i])+bbx[0,i]

	return himg,bbx

def VerticalFlip(img,bbox):
	vimg = cv2.flip(img, 0)