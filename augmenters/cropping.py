import numpy as np 
import cv2 

def SingleCropping(img, size, objct, bbox, **kwargs):

	total_w = size[0]
	total_h = size[1]
	
	Width = 600
	Height = 600

	imgs = []
	vals = []
	coords = []
	
	xmin = []
	ymin = []
	xmax = []
	ymax = []

	pose = []
	truncated = []
	difficult = []
	label = []

	if ('Width' in kwargs):
		Width = kwargs['Width']

	if ('Heigth' in kwargs):
		Height = kwargs['Heigth']
	
	if ('Orientation' in kwargs):

		if (kwargs['Orientation'] == 'Center'):
			
			for i in range(objct.shape[1]):
				diffx = int((Width-(bbox[2,i]-bbox[0,i]))/2)
				diffy = int((Height-(bbox[3,i]-bbox[1,i]))/2)

				if((bbox[2,i]+diffx)>=total_w):
					Np = total_w
					N = Np-Width

				elif((bbox[0,i]-diffx)<=0):
					N = 0
					Np = N+Width
				
				else: 
					N = bbox[0,i]-diffx
					Np = N+Width


				if((bbox[3,i]+diffy)>=total_h):
					mp = total_h
					m = mp-Height

				elif((bbox[1,i]-diffy)<=0):
					m = 0
					mp = m+Height
				
				else: 
					m = bbox[1,i]-diffy
					mp = m+Height

				temporal = img[m:mp, N:Np]
				
				a = bbox[0,i]-N
				b = bbox[1,i]-m
				c = a+(bbox[2,i]-bbox[0,i])
				d = b+(bbox[3,i]-bbox[1,i]) 
				
				xmin.append(a) 
				ymin.append(b)
				xmax.append(c)
				ymax.append(d)

				imgs.append(temporal)
				
				label.append(objct[0,i])
				pose.append(objct[1,i])
				truncated.append(objct[2,i])
				difficult.append(objct[3,i])
			
		elif(kwargs['Orientation'] == 'Random'):
			for i in range(objct.shape[1]):
				Varx = Width-(bbox[2,i]-bbox[0,i])
				Vary = Height-(bbox[3,i]-bbox[1,i])
				if (Varx<=0):
					Varx=1

				if (Vary<=0):
					Vary=1					

				Diffx = int(np.random.randint(0,Varx))
				restx = Varx-Diffx  

				Diffy = int(np.random.randint(0,Vary))
				resty = Vary-Diffy

				if ((bbox[2,i]+restx)>=total_w):
					Np = total_w
					N = Np-Width 

				elif((bbox[0,i]-Diffx)<=0):
					N=0
					Np=N+Width
				
				else: 
					N=bbox[0,i]-Diffx
					Np=N+Width


				if ((bbox[3,i]+resty)>=total_h):
					mp = total_h
					m = mp-Height 

				elif((bbox[1,i]-Diffy)<=0):
					m=0
					mp=m+Height
				
				else: 
					m=bbox[1,i]-Diffy
					mp=N+Height

				temporal = img[m:mp, N:Np]

				a = bbox[0,i]-N
				b = bbox[1,i]-m
				c = a+(bbox[2,i]-bbox[0,i])
				d = b+(bbox[3,i]-bbox[1,i]) 

				xmin.append(a) 
				ymin.append(b)
				xmax.append(c)
				ymax.append(d)

				imgs.append(temporal)
				
				label.append(objct[0,i])
				pose.append(objct[1,i])
				truncated.append(objct[2,i])
				difficult.append(objct[3,i])

	xmin = np.array(xmin)
	ymin = np.array(ymin)
	xmax = np.array(xmax)
	ymax = np.array(ymax)

	vals.append(label)
	vals.append(pose)
	vals.append(truncated)
	vals.append(difficult)

	vals = np.array(vals)
	imgs = np.array(imgs)
	coords = np.array([xmin,ymin,xmax,ymax])

	return imgs, vals, coords

def MultipleCropping(img, size, objct, bbox, **kwargs):

	total_w = size[0]
	total_h = size[1]
	
	Width = 300
	Height = 300

	aux = []
	imgs = []
	
	sdt = []
	if ('Width' in kwargs):
		Width = kwargs['Width']

	if ('Heigth' in kwargs):
		Height = kwargs['Heigth']

	for i in range(objct.shape[1]):
		
		vals = []
		coords = []

		xmin = []
		ymin = []
		xmax = []
		ymax = []
		Object = []
		pose = []
		truncated = []
		difficult = []
		label = []

		if (i in aux):
			continue

		else: 
			Varx = Width-(bbox[2,i]-bbox[0,i])
			Vary = Height-(bbox[3,i]-bbox[1,i])					
			if (Varx<=0):
				Varx=1

			if (Vary<=0):
				Vary=1
			Diffx = int(np.random.randint(0,Varx))
			restx = Varx-Diffx  

			Diffy = int(np.random.randint(0,Vary))
			resty = Vary-Diffy

			if ((bbox[2,i]+restx)>=total_w):
				Np = total_w
				N = Np-Width 

			elif((bbox[0,i]-Diffx)<=0):
				N=0
				Np=N+Width
			
			else: 
				N=bbox[0,i]-Diffx
				Np=N+Width


			if ((bbox[3,i]+resty)>=total_h):
				mp = total_h
				m = mp-Height 

			elif((bbox[1,i]-Diffy)<=0):
				m=0
				mp=m+Height
			
			else: 
				m=bbox[1,i]-Diffy
				mp=m+Height

			temporal = img[m:mp, N:Np]

			a = bbox[0,i]-N
			b = bbox[1,i]-m
			c = a+(bbox[2,i]-bbox[0,i])
			d = b+(bbox[3,i]-bbox[1,i])
		
			xmin.append(a) 
			ymin.append(b)
			xmax.append(c)
			ymax.append(d)

			imgs.append(temporal)
			
			label.append(objct[0,i])
			pose.append(objct[1,i])
			truncated.append(objct[2,i])
			difficult.append(objct[3,i])

			aux.append(i)

			for j in range(objct.shape[1]):
				
				if (j in aux): 
					continue

				else: 
					if (bbox[0,j]>=N and bbox[0,j]<=Np-(int((bbox[2,j]-bbox[0,j])/2))):
						
						if (bbox[1,j]>=m and bbox[1,j]<=mp-(int((bbox[3,j]-bbox[1,j])/2))):
							xmin.append(bbox[0,j]-N)
							ymin.append(bbox[1,j]-m)

							if (bbox[2,j]>=Np):
								xmax.append(Width)
								label.append(objct[0,j])
								pose.append(objct[1,j])
								truncated.append(objct[2,j])
								difficult.append(objct[3,j])

								if(bbox[3,j]>=mp):
									ymax.append(Height)
									aux.append(j)
									continue
								else:
									ymax.append(bbox[3,j]-m)
									aux.append(j)
									continue
																
							else: 
								xmax.append(bbox[2,j]-N)
								label.append(objct[0,j])
								pose.append(objct[1,j])
								truncated.append(objct[2,j])
								difficult.append(objct[3,j])							
								
								if(bbox[3,j]>=mp):
									ymax.append(Height)
									aux.append(j)
									continue
								else:
									ymax.append(bbox[3,j]-m)
									aux.append(j)
									continue

						elif(bbox[1,j]<m):
							
							if(bbox[3,j]>m+(int((bbox[3,j]-bbox[1,j])/2))):
								label.append(objct[0,j])
								pose.append(objct[1,j])
								truncated.append(objct[2,j])
								difficult.append(objct[3,j])
								xmin.append(bbox[0,j]-N)
								ymin.append(0)

								if(bbox[2,j]>=Np):
									xmax.append(Width)
								else:
									xmax.append(bbox[2,j]-N)

								if(bbox[3,j]>=mp):
									ymax.append(Height)
								else:
									ymax.append(bbox[3,j]-m)	
	
								aux.append(j)
								continue

							else:
								continue
						else:
							continue

					elif(bbox[0,j]<N):
						if(bbox[2,j]>N+(int((bbox[2,j]-bbox[0,j])/2))):
							
							if(bbox[1,j]<m):
								if(bbox[3,j]>m+(int((bbox[3,j]-bbox[1,j])/2))):
									xmin.append(0)
									ymin.append(0)
									xmax.append(bbox[2,j]-N)
									ymax.append(bbox[3,j]-m)
									label.append(objct[0,j])
									pose.append(objct[1,j])
									truncated.append(objct[2,j])
									difficult.append(objct[3,j])
									aux.append(j)
									continue 
								else:
									continue

							elif(bbox[1,j]>=m and bbox[3,j]<=mp):
								xmin.append(0)
								ymin.append(bbox[1,j]-m)
								xmax.append(bbox[2,j]-N)
								ymax.append(bbox[3,j]-m)
								label.append(objct[0,j])
								pose.append(objct[1,j])
								truncated.append(objct[2,j])
								difficult.append(objct[3,j])
								aux.append(j)
								continue

							else:
								if(bbox[1,j]<=mp-(int((bbox[3,j]-bbox[1,j])/2))):
									xmin.append(0)
									ymin.append(bbox[1,j]-m)
									xmax.append(bbox[2,j]-N)
									ymax.append(Height)
									label.append(objct[0,j])
									pose.append(objct[1,j])
									truncated.append(objct[2,j])
									difficult.append(objct[3,j])
									aux.append(j)
									continue 

								else: 
									continue
						else:
							continue
					else:
						continue

		xmin = np.array(xmin)
		ymin = np.array(ymin)
		xmax = np.array(xmax)
		ymax = np.array(ymax)

		label=np.array(label)
		pose=np.array(pose)
		truncated=np.array(truncated)
		difficult=np.array(difficult)

		vals = np.array([label,pose,truncated,difficult])
		coords = np.array([xmin,ymin,xmax,ymax])

		Object.append(coords)
		Object.append(vals)
		
		sdt.append(Object)

	imgs = np.array(imgs)

	return sdt, imgs


