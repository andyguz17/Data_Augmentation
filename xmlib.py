from lxml import etree as et
import numpy as np 
import cv2 
import os

def reader(doc_path):

	tree = et.parse(doc_path)

	objct = []

	database = ''
	width = 0 
	height = 0
	depth = 0
	segmented = ''
	
	pose = []
	truncated = []
	difficult = []
	label = []

	xmin = []
	ymin = []
	xmax = []
	ymax = []

	root = tree.getroot()

	for element in root: 
		if (element.tag == 'folder'):
			folder = element.text
			 
		elif (element.tag == 'filename'):   
			filename = element.text
		
		elif (element.tag == 'path'):
			path = element.text
			
		elif (element.tag == 'source'):
			for sub in element:
				database=sub.text
				
		elif (element.tag == 'size'):
			for dim in element:
				if (dim.tag == 'width'):
					width=int(dim.text)
					
				elif (dim.tag == 'height'):
					height=int(dim.text)
					
				elif (dim.tag == 'depth'):
					depth=int(dim.text)
					
		elif (element.tag == 'segmented'):
			segmented = element.text
			
		elif (element.tag == 'object'):
			
			for objects in element: 
				if(objects.tag == 'name'):
					label.append(objects.text)
					
				elif(objects.tag == 'pose'):
					pose.append(objects.text)
					
				elif(objects.tag == 'truncated'):
					truncated.append(objects.text)
					
				elif(objects.tag == 'difficult'):
					difficult.append(objects.text)
					
				elif(objects.tag == 'bndbox'):
					for coords in objects:
						if (coords.tag == 'xmin'):
							xmin.append(int(coords.text))                         

						elif (coords.tag == 'ymin'):
							ymin.append(int(coords.text))                             

						elif (coords.tag == 'xmax'):
							xmax.append(int(coords.text))                    

						elif (coords.tag == 'ymax'): 
							ymax.append(int(coords.text))
	
	size = np.array([width,height,depth])

	xmin = np.array(xmin)
	ymin = np.array(ymin)
	xmax = np.array(xmax)
	ymax = np.array(ymax)
	
	objct.append(label)
	objct.append(pose)
	objct.append(truncated)
	objct.append(difficult)

	objct = np.array(objct)
	bbox = np.array([xmin,ymin,xmax,ymax])
	
	return folder, filename, path, database, size, segmented, objct, bbox

def writer(folder, filename, path, database, size, segmented, objct, bbox, annotation_path): 

	root = et.Element('annotation')
	
	fol = et.SubElement(root,'folder')
	fol.text = str(folder)
	file = et.SubElement(root,'filename')
	file.text = str(filename)

	pth = et.SubElement(root,'path')
	pth.text = str(path)

	src = et.SubElement(root,'source')
	datab = et.SubElement(src,'database')
	datab.text = str(database)

	dim = et.SubElement(root,'size')
	w = et.SubElement(dim,'width')
	w.text = str(size[0])
	h = et.SubElement(dim,'height')
	h.text = str(size[1])
	d = et.SubElement(dim,'depth')
	d.text = str(size[2])

	segment = et.SubElement(root,'segmented')
	segment.text = str(segmented) 

	for i in range(objct.shape[1]):

		obj = et.SubElement(root, 'object')
		name = et.SubElement(obj,'name')
		name.text = str(objct[0,i])

		pose = et.SubElement(obj,'pose')
		pose.text = str(objct[1,i])
		
		truncated = et.SubElement(obj,'truncated')
		truncated.text = str(objct[2,i])
		
		difficult = et.SubElement(obj,'difficult')
		difficult.text = str(objct[3,i])
		
		bndbox = et.SubElement(obj,'bndbox')
		xmin = et.SubElement(bndbox,'xmin')
		xmin.text = str(bbox[0,i])
		ymin = et.SubElement(bndbox,'ymin')
		ymin.text = str(bbox[1,i])
		xmax = et.SubElement(bndbox,'xmax')
		xmax.text = str(bbox[2,i])
		ymax = et.SubElement(bndbox,'ymax')
		ymax.text = str(bbox[3,i])
		
	string = et.tostring(root, pretty_print=True)

	(image_name, extension) = os.path.splitext(filename)
	new_path = os.path.join(annotation_path,image_name+'.xml')
	filew = open(new_path, "wb")
	filew.write(string)
	filew.close()