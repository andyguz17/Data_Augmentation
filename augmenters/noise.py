import numpy as np 
import cv2 

def GaussianNoise(image,**kwargs):

	temp_image = np.float64(np.copy(image))

	h = temp_image.shape[0]
	w = temp_image.shape[1]

	mean = 0
	sigma = 0.05

	if ('mean' in kwargs):
		mean = kwargs['mean']

	if ('sigma' in kwargs):
		sigma = kwargs['sigma']

	noise = np.random.normal(mean,sigma,(h, w))

	noisy_image = np.zeros(temp_image.shape, np.float64)

	noisy_image[:,:,0] = temp_image[:,:,0]/255 + noise
	noisy_image[:,:,1] = temp_image[:,:,1]/255 + noise
	noisy_image[:,:,2] = temp_image[:,:,2]/255 + noise

	cv2.normalize(noisy_image, noisy_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)

	return noisy_image.astype(np.uint8)

def Salt_Pepper(image):

	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	row,col = image.shape
	s_vs_p = 0.5
	amount = 0.04
	out = np.copy(image)

	print(image.shape)
	# Salt mode
	num_salt = np.ceil(amount * image.size * s_vs_p)
	coords = [np.random.randint(0, i-1, int(num_salt))for i in image.shape]
	out[coords] = 255

	# Pepper mode
	num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
	coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
	out[coords] = 0

	out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)

	return out