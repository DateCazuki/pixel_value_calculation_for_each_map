#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import csv
import numpy as np
import skimage.util
import matplotlib.pyplot as plt

CurrentDirPath = os.getcwd()

def area_split(rawpath):
    width = 9600
    height = 6437
    fd = open(rawpath,'rb')
    f = np.fromfile(fd,dtype=np.int16,count=width*height)
    img = f.reshape((height,width))
    fd.close()
    epa  = img[48:6428,24:9594] #画像分割のためにHV方向に5等分できるようエリア抽出する．
    opbh = img[14:48,24:9594]    #画像分割のためにH方向に5等分できるようエリア抽出する．
    opbv = img[48:6428,0:24]    #画像分割のためにV方向に5等分できるようエリア抽出する．
    return opbh,opbv,epa

#　引数となる画像に対してRGB各成分の画素を抜き取りするDebayer．
#  ただし，引数となる画像の左上画素はR，右下画素はBでなければならない．
def debayer(img):
    img_red=img[::2,::2]
    img_greenred=img[::2,1::2] #Gr=Gbとみなす．
    img_blue=img[1::2,1::2]
    return img_red,img_greenred,img_blue

def mean_record(rawfile,blocks_epa,blocks_opb_h,blocks_opb_v,txtfile):
    with open(txtfile,'a') as f:
        print(rawfile, end='\t', file=f)
        for y in range(5):
            for x in range(5):
                print(np.mean(blocks_epa[x,y]),end='\t',file=f)
                
        for y in range(5):
            print(np.mean(blocks_opb_h[0,y]),end='\t',file=f)
        
        for x in range(5):
            print(np.mean(blocks_opb_v[x,0]),end='\t',file=f)
        
        print('',file=f)

def item_record(txtfile):
    with open(txtfile,'a') as f:
        print('RawFileName', end='\t', file=f)
        for y in range(5):
            for x in range(5):
                print('blocks_epa[{}{}]'.format(x,y),end='\t',file=f)
                
        for y in range(5):
                print('blocks_opb_h[{}{}]'.format(x,y),end='\t',file=f)
        
        for x in range(5):
                print('blocks_opb_v[{}{}]'.format(x,y),end='\t',file=f)
        
        print('',file=f)
        
        
def patch_pixval(rawfile):
    opb_h,opb_v,epa = area_split(rawfile)
    opb_h_r,opb_h_g,opb_h_b = debayer(opb_h)
    opb_v_r,opb_v_g,opb_v_b = debayer(opb_v)
    epa_r,  epa_g,  epa_b   = debayer(epa)
        
    blocks_opb_h_r = skimage.util.view_as_blocks(opb_h_r, (opb_h_r.shape[0], opb_h_r.shape[1]//5))
    blocks_opb_h_g = skimage.util.view_as_blocks(opb_h_g, (opb_h_g.shape[0], opb_h_g.shape[1]//5))
    blocks_opb_h_b = skimage.util.view_as_blocks(opb_h_b, (opb_h_b.shape[0], opb_h_b.shape[1]//5))

    blocks_opb_v_r = skimage.util.view_as_blocks(opb_v_r, (opb_v_r.shape[0]//5, opb_v_r.shape[1]))
    blocks_opb_v_g = skimage.util.view_as_blocks(opb_v_g, (opb_v_g.shape[0]//5, opb_v_g.shape[1]))
    blocks_opb_v_b = skimage.util.view_as_blocks(opb_v_b, (opb_v_b.shape[0]//5, opb_v_b.shape[1]))
    
    blocks_epa_r   = skimage.util.view_as_blocks(epa_r, (epa_r.shape[0]//5, epa_r.shape[1]//5))
    blocks_epa_g   = skimage.util.view_as_blocks(epa_g, (epa_g.shape[0]//5, epa_g.shape[1]//5))
    blocks_epa_b   = skimage.util.view_as_blocks(epa_b, (epa_b.shape[0]//5, epa_b.shape[1]//5))

    mean_record(rawfile,blocks_epa_r,blocks_opb_h_r,blocks_opb_v_r,'r.txt')
    mean_record(rawfile,blocks_epa_g,blocks_opb_h_g,blocks_opb_v_g,'g.txt')
    mean_record(rawfile,blocks_epa_b,blocks_opb_h_b,blocks_opb_v_b,'b.txt')

def ProgressiveScan(path):
    item_record('r.txt')
    item_record('g.txt')
    item_record('b.txt')
    for curDir,dirs,files in os.walk(path):
        for rawfile in files:
            if rawfile.endswith('.raw'):
                patch_pixval(rawfile)
            
ProgressiveScan(CurrentDirPath)


# In[ ]:




