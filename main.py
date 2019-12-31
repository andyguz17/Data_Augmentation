from augmenters import cropping as crp
from augmenters import flipping as flp
from augmenters import noise as ns 
from augmenters import tonality as tn 
import numpy as np 
import xmlib
import cv2  
import os

def dataCreation(Width, Height, name, **kwargs):
	####################
	#######PATHS########
	####################

	if not os.path.exists(name):
		os.makedirs(name)

	annp = os.path.join(os.getcwd(),'data')
	annpr = os.path.join(os.getcwd(),name)

	####################
	#######PATHS########
	####################

	glblctr = 0
	mode = 'Center'

	if ('Orientation' in kwargs):
		mode =  kwargs['Orientation']

	for doc in (os.listdir(annp)):
		if doc.endswith('.xml'):

			folder, filename, path, database, size, segmented, objct, bbox = xmlib.reader(os.path.join(annp,doc))
			
			auxa = []
			auxb = []

			auxbbxa = []
			auxbbxb = []

			im = cv2.imread(path)
			
			auxa.append(im)
			auxb.append(im)
			auxbbxa.append(bbox)
			auxbbxb.append(bbox)

			if ('Tonality' in kwargs):
				if (kwargs['Tonality'] == True):
					ton = tn.pca(im)
					auxa.append(ton)
					auxb.append(ton)
					auxbbxa.append(bbox)
					auxbbxb.append(bbox)

			if('Noise' in kwargs):
				if (kwargs['Noise'] == True):
					
					if (kwargs['Nmode'] == 'Gauss'):	

						if (kwargs['Tonality'] == True):
							Gimg = ns.GaussianNoise(im)
							Gton = ns.GaussianNoise(ton)
							auxa.append(Gimg)
							auxa.append(Gton)
							auxbbxa.append(bbox)
							auxbbxa.append(bbox)
			
							auxb.append(Gimg)
							auxb.append(Gton)
							auxbbxb.append(bbox)
							auxbbxb.append(bbox)

						else: 
							Gimg = ns.GaussianNoise(im)
							auxa.append(Gimg)
							auxb.append(Gimg)
							auxbbxa.append(bbox)
							auxbbxb.append(bbox)

			auxa = np.array(auxa)
			auxbbxa = np.array(auxbbxa)

			if ('Flip' in kwargs):
				if (kwargs['Flip'] == True):
					if (kwargs['Fmode'] == 'Horizontal'):				
						
						for m in range(auxa.shape[0]):
							newim, newbbx =  flp.HorizontalFlip(auxa[m],auxbbxa[m])
							auxb.append(newim)
							auxbbxb.append(newbbx)
						
			auxb = np.array(auxb)
			auxbbxb = np.array(auxbbxb)
			
			if ('Crop' in kwargs):
				if (kwargs['Crop'] == True):

					if(kwargs['Cmode'] == 'Single'):

						for j in range(auxb.shape[0]):
							images,vals,coords = crp.SingleCropping(auxb[j],size,objct,auxbbxb[j],
																   Orientation = mode,
																   Width = Width,
																   Heigth = Height) 

							for i in range(images.shape[0]):
								
								newname = 'img_'+str(glblctr)+'.jpg'
								newpath = os.path.join(annpr, newname)
								newSize = np.array([Width,Height,3])

								xmlib.writer(name, newname, newpath, database, newSize, segmented, np.array([vals[:,i]]).T, np.array([coords[:,i]]).T, annpr)
								cv2.imwrite(newpath, images[i])
								glblctr+=1
								print(newname)


					elif(kwargs['Cmode']=='Multiple'):
							
							for j in range(auxb.shape[0]):
								obj, img = crp.MultipleCropping(auxb[j],size,objct,auxbbxb[j],
																Width = Width,
																Heigth = Height) 

								for i in range(len(obj)):

									a = np.array(obj[i][0])#boundingBox
									b = np.array(obj[i][1])#Objct
									#print(a.shape)
									#print(b.shape)
									
									newname = 'img_'+str(glblctr)+'.jpg'
									newpath = os.path.join(annpr,newname)
									newSize = np.array([Width,Height,3])

									xmlib.writer(name, newname,newpath, database, newSize, segmented, b, a, annpr)
									cv2.imwrite(newpath, img[i])
									glblctr+=1
									print(newname)

				else: 
					for j in range(auxb.shape[0]):
						newname = 'img_'+str(glblctr)+'.jpg'
						newpath = os.path.join(annpr,newname)
						newSize = np.array([im.shape[1],im.shape[0],3])

						xmlib.writer(name, newname,newpath, database, newSize, segmented, objct, auxbbxb[j], annpr)
						cv2.imwrite(newpath, auxb[j])
						glblctr+=1
						print(newname)
		else: 									
			continue

def visualizeData(name):

	font = cv2.FONT_HERSHEY_SIMPLEX
	dpath = os.path.join(os.getcwd(),name)
	
	for doc in (os.listdir(dpath)):
		if doc.endswith('.xml'):

			folder, filename, path, database, size, segmented, objct, bbox = xmlib.reader(os.path.join(dpath,doc))
			im = cv2.imread(path)

			for i in range(bbox.shape[1]):
				cv2.rectangle(im, (bbox[0,i], bbox[1,i]), (bbox[2,i],bbox[3,i]), (160,30,80), 3)
				cv2.putText(im,objct[0,i] ,(int((bbox[2,i]-bbox[0,i])/2+bbox[0,i])-10,bbox[1,i]-5), font, 1,(150,150,58),2,cv2.LINE_AA)

			cv2.imshow('a',im)
			cv2.waitKey()
			cv2.destroyAllWindows()


if __name__ == "__main__":
	
	#visualizeData('data_1')
	#visualizeData('data_2')
	visualizeData('data_3')
	#visualizeData('data_4')
	
	"""
	dataCreation(600,600,'data_4',
				Tonality = True,
				Noise = True, 
				Nmode = 'Gauss',
				Crop = False, 
				Flip = True, 
				Fmode = 'Horizontal')
	
	dataCreation(600,600,'data_1',
				Tonality = True,
				Noise = True, 
				Nmode = 'Gauss',
				Crop = True, 
				Cmode = 'Single', 
				Orientation = 'Center',
				Flip = True, 
				Fmode = 'Horizontal')
	print("-----------------------")
	dataCreation(900,900,'data_2',
				Tonality = True,
				Noise = True, 
				Nmode = 'Gauss',
				Crop = True, 
				Cmode = 'Single', 
				Orientation = 'Random',
				Flip = True, 
				Fmode = 'Horizontal')
	print("-----------------------")
	
	dataCreation(600,600,'data_3',
				Tonality = True,
				Noise = True, 
				Nmode = 'Gauss',
				Crop = True, 
				Cmode = 'Multiple', 
				Flip = True, 
				Fmode = 'Horizontal')
	"""