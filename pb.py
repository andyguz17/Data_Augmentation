#Prueba 
from augmenters import noise as ns 
from augmenters import tonality as tn 
import numpy as np
import cv2 
import os 
"""
a = np.array([[6,7,8]])
m = np.array(([[4,5,6],[7,8,9]]))
img = np.zeros([5,5])

vara = m[:,0]
varb = np.array([m[:,0]])

print(m.shape)
print(varb.shape)

s = []

s.append(a)
s.append(m)
s.append(img)

for i in range(len(s)):
	print(s[i])
	print("'''''''''''")
"""

imp = os.path.join(os.getcwd(),'data')

img = cv2.imread(os.path.join(imp,('img_0.jpg')))

img = cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))

#a = ns.GaussianNoise(img) 
#b = ns.Salt_Pepper(img)

for i in range (10):

	a =tn.pca(img)
	cv2.imshow('asd',img)
	cv2.imshow('ard',a)
	#cv2.imshow('arw',b)
	cv2.waitKey()
	cv2.destroyAllWindows()

