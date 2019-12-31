from lxml import etree as et 
import os 
import time 
import cv2 
import numpy as np

def xml_writer(folder, filename, path, database, size, segmented, objct, bbox, annotation_path): 

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

    obj = et.SubElement(root, 'object')
    name = et.SubElement(obj,'name')
    name.text = str(objct[0])

    pose = et.SubElement(obj,'pose')
    pose.text = str(objct[1])
    
    truncated = et.SubElement(obj,'truncated')
    truncated.text = str(objct[2])
    
    difficult = et.SubElement(obj,'difficult')
    difficult.text = str(objct[3])
    
    bndbox = et.SubElement(obj,'bndbox')
    xmin = et.SubElement(bndbox,'xmin')
    xmin.text = str(bbox[0])
    ymin = et.SubElement(bndbox,'ymin')
    ymin.text = str(bbox[1])
    xmax = et.SubElement(bndbox,'xmax')
    xmax.text = str(bbox[2])
    ymax = et.SubElement(bndbox,'ymax')
    ymax.text = str(bbox[3])
    
    string = et.tostring(root, pretty_print=True)

    (image_name, extension) = os.path.splitext(filename)
    new_path = os.path.join(annotation_path,image_name+'.xml')
    filew = open(new_path, "wb")
    filew.write(string)
    filew.close()


path = os.path.join(os.getcwd(),'notes') 
ctr = 0
font = cv2.FONT_HERSHEY_SIMPLEX
CtteX = 600
CtteY = 500

if not os.path.exists('main'):
        os.makedirs('main')

for i,name in enumerate(os.listdir(path)):
    
    (image_name, extension) = os.path.splitext(name)
    
    if(extension == ".xml"):

        objctr = 0
        xml_file = os.path.join(path,name)
        tree = et.parse(xml_file)

        #############
        ##VARAIBLES##
        #############

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
        
        
        #############
        ##VARAIBLES##
        #############
        root = tree.getroot()

        for element in root: 

            if (element.tag == 'folder'):
                folder = element.text
                print('folder:\t'+folder)
         
            elif (element.tag == 'filename'):   
                im_name = element.text
                print('archivo:\t'+im_name)

            elif (element.tag == 'path'):
                im_path = element.text
                print(im_path)

            elif (element.tag == 'source'):
                for sub in element:
                    database=sub.text
                    print(database)

            elif (element.tag == 'size'):
                for dim in element:
                    if (dim.tag == 'width'):
                        width=int(dim.text)
                        print("Ancho:\t"+str(width))

                    elif (dim.tag == 'height'):
                        height=int(dim.text)
                        print("Altura:\t"+str(height))

                    elif (dim.tag == 'depth'):
                        depth=int(dim.text)
                        print("Profundidad:\t"+str(depth))

            elif (element.tag == 'segmented'):
                segmented = element.text
                print('segmented:\t'+element.text)

            elif (element.tag == 'object'):
                print('*******************************')
                for objects in element: 
                    if(objects.tag == 'name'):
                        label.append(objects.text)
                        print('label:\t'+objects.text)
                    elif(objects.tag == 'pose'):
                        pose.append(objects.text)
                        print('pose:\t'+objects.text)
                    elif(objects.tag == 'truncated'):
                        truncated.append(objects.text)
                        print('truncated:\t'+objects.text)
                    elif(objects.tag == 'difficult'):
                        difficult.append(objects.text)
                        print('difficult:\t'+objects.text)
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

        print("\n\n")
        temporal = cv2.imread(im_path)
        original = np.copy(temporal)

        xmin=np.array(xmin)
        ymin=np.array(ymin)
        xmax=np.array(xmax)
        ymax=np.array(ymax)

        print('xmin:\t'+str(xmin))
        print('ymin:\t'+str(ymin))
        print('xmax:\t'+str(xmax))
        print('ymax:\t'+str(ymax))
        

        for i in range(xmin.shape[0]):
            #cv2.rectangle(temporal, (xmin[i], ymin[i]), (xmax[i], ymax[i]), (30,160,80), 5)
            #cv2.putText(temporal,label[i] ,(int((xmax[i]-xmin[i])/2+xmin[i])-10,ymin[i]-5), font, 1,(150,150,58),2,cv2.LINE_AA)

            diffw =  width - xmin[i]
            diffh = height - ymin[i]
            temp_width = xmax[i]-xmin[i]
            temp_height = ymax[i]-ymin[i]

            if (diffw >= CtteX):
            	if (xmax[i]<=CtteX):
            		x = int(np.random.uniform(0,xmin[i]))
            	
            	else:
            		x = int(np.random.uniform(xmax[i]-CtteX, xmin[i]))
            else: 
            	x = int(np.random.uniform(xmax[i]-CtteX, width-CtteX))

            if (diffh >= CtteY):
            	if(ymax[i]<=CtteY):
            		y = int(np.random.uniform(0,ymin[i]))

            	else:
            			y = int(np.random.uniform(ymax[i]-CtteY, ymin[i]))
            else: 
            	y = int(np.random.uniform(ymax[i]-CtteY, height-CtteY))

            VarX = xmin[i]-x
            VarY = ymin[i]-y
            
            crop_temp=temporal[y:y+CtteY, x:x+CtteX]
            
            #cv2.rectangle(temporal, (x, y), (x+CtteX,y+CtteY), (160,30,80), 3)
            #cv2.rectangle(crop_temp, (VarX, VarY), (VarX+temp_width,VarY+temp_height), (50,30,160), 3)
            
            if not os.path.exists('main/images'):
                    os.makedirs('main/images')

            if not os.path.exists('main/annotations'):
                    os.makedirs('main/annotations')
            
            ctr+=1

            """
            cv2.imwrite('main/images/data_'+str(ctr)+'.jpg', crop_temp) 
            
            images_path = os.path.join(os.getcwd(),'main','images','data_'+str(ctr)+'.jpg')
            annotation_path = os.path.join(os.getcwd(),'main','annotations')
 
            size = [crop_temp.shape[1],crop_temp.shape[0],crop_temp.shape[2]]
            args = [label[i],pose[i],truncated[i],difficult[i]] 
            bbox = [VarX,VarY,VarX+temp_width,VarY+temp_height]           
            xml_writer('images','data_'+str(ctr)+'.jpg',images_path, database, size, segmented, args, bbox,annotation_path)
            """    
            cv2.imshow('crop',crop_temp)
            cv2.waitKey()
            cv2.destroyAllWindows()
            
