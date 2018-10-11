# -*- coding: UTF-8 -*-
from pycocotools.coco import COCO
import numpy as np
import cv2

#需要训练的类别
train_cls = ["person", "cat" , "dog", "bicycle", "boat", "bus" , "truck", "car", "motorcycle"]

#写label txt文件夹路径
label_file = "labels"

dataType = "train2017"
#coco数据集json标签路径
annFile = "annotations/instances_%s.json"%dataType
print annFile

#调用coco api加载json文件
coco = COCO(annFile)

#获取数据集的类别及对应id(下标),并创建dict,key=name,vaule=id;
cls_dict={}
cats = coco.loadCats(coco.getCatIds())
for n in cats:
    cls_dict[n["id"]] = n["name"]

#获取图像id
imgIds = coco.getImgIds()
for i in imgIds:
    #获取图像的信息,文件名,长,宽
    img_inf = coco.loadImgs(i)
    file_name = img_inf[0]["file_name"]
    width = img_inf[0]["width"]
    height = img_inf[0]["height"]
    #print file_name, width, height

    dw = 1./(width)
    dh = 1./(height)

    #print dw , dh

    #获取图像标签信息,bbox，类别id
    anno_ids = coco.getAnnIds(imgIds=i, iscrowd=None)
    anno = coco.loadAnns(anno_ids)

    #加载图像
    images = cv2.imread("images/%s/%s"%(dataType,file_name))
    print "images/%s/%s"%(dataType,file_name)

    for label in anno:
        #获取检测框坐标(xl,yl,w,h),以及对应的类别id
        bbox = label["bbox"]
        name_id =  label["category_id"]
    
        #如果检测框类别是需要的训练类别
        if cls_dict[name_id] in train_cls:
            #调用opencv画出检测框[调试用]
            id = train_cls.index(cls_dict[name_id])

            #cv2.rectangle(images, (int(bbox[0]),int(bbox[1])), (int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])), (255, 245,0), 2)
            #cv2.putText(images, str(id), (int(bbox[0]),int(bbox[1])), 0, 0.7, (0, 255, 0), 2)

            x_c = (bbox[0]+(bbox[2]/2.0))*dw
            y_c = (bbox[1]+(bbox[3]/2.0))*dh
            w = bbox[2]*dw
            h = bbox[3]*dh
            #print id,x_c,y_c,w,h
            #写标签文件
            with open('%s/%s/%s.txt'%(label_file,dataType,file_name[:-4]), 'a+') as f:
                f.write(str(id)+" "+str(x_c)+" "+str(y_c)+" "+str(w)+" "+str(h)+"\n")
    #cv2.imshow("capture", images)
    #cv2.waitKey(0)
