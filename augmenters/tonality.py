import numpy as np 
import cv2 


def pca(img):

	w = img.shape[1]
	h = img.shape[0]
	
	im = np.copy(img)/255
	matrB = np.array(im[:,:,0],dtype=float)
	matrG = np.array(im[:,:,1],dtype=float)
	matrR = np.array(im[:,:,2],dtype=float)

	############
	####BLUE####
	############
	mXB=matrB-np.kron(((matrB[:,:].transpose()).transpose()).mean(),np.ones((1,w),dtype=float))
	uB, sB, vhB = np.linalg.svd(mXB, full_matrices=True)

	VB = np.copy(uB)
	prodB = np.dot(np.dot(VB,VB.transpose()),matrB)


	#############
	####GREEN####
	#############
	mXG=matrG-np.kron(((matrG[:,:].transpose()).transpose()).mean(),np.ones((1,w),dtype=float))
	uG, sG, vhG = np.linalg.svd(mXG, full_matrices=True)

	VG = np.copy(uG)
	prodG = np.dot(np.dot(VG,VG.transpose()),matrG)


	###########
	####RED####
	###########
	mXR=matrR-np.kron(((matrR[:,:].transpose()).transpose()).mean(),np.ones((1,w),dtype=float))
	uR, sR, vhR = np.linalg.svd(mXR, full_matrices=True)

	VR = np.copy(uR)
	prodR = np.dot(np.dot(VR,VR.transpose()),matrR)

	mu = 0
	sigma = 0.1 
	s1 = np.random.normal(mu, sigma)
	s2 = np.random.normal(mu, sigma)
	s3 = np.random.normal(mu, sigma)
	
	im[:,:,0] = im[:,:,0]+prodB*s3
	im[:,:,1] = im[:,:,1]+prodG*s2
	im[:,:,2] = im[:,:,2]+prodR*s1
		
	cv2.normalize(im, im, 0, 255, cv2.NORM_MINMAX, dtype=-1)

	im=cv2.resize(im,(img.shape[1],img.shape[0]))

	return im.astype(np.uint8)
