#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 22:38:02 2020

@author: yuan
"""

import openpyxl #连接excel
import requests #下载图片
import base64   #对图片进行加密
from aip import AipFace #加载人脸识别
import json #输出格式
import shutil #移动图片
import os #删除、创建文件
import os.path
#获取工作薄对象
workbook = openpyxl.load_workbook("C://Users/PANSAFE/Documents/Tencent Files/2984555408/FileRecv/MobileFile/media.xlsx")

#获取所有工作表名
shenames = workbook.sheetnames

#获取第一个工作表
worksheet = workbook['Sheet2']
num = 0
#获取每一行
for row in worksheet.rows:
    #print(row)#代表一行的每一个单元格地址
    #获取每一行第二个元素，这里是url地址
    image_url = row[4].value
    #去掉空值
    if 'http' in image_url : #去掉空值
        print(image_url) 
        #获取图片数据
        #判断网页响应
        headers = { 'Connection': 'close',}
        response = requests.get(image_url,headers=headers,proxies={"http":"127.0.0.1:8118"})
        img_data = requests.get(image_url).content
        #如果不是200则过滤，并打印返回值
        if  not response.ok:
            print(response)
        else:
            #给图片创建文件名
            dirs = row[1].value
            name = str(num)
            loc = '{row1}|{row2}.jpeg'.format(row1 = row[0].value,row2 = name)
            print(dirs+'/'+loc)
            num = num + 1
            if not os.path.isfile(dirs+'/'+loc):
            #创建这个文件
                with open(loc, 'wb') as handler:
                    #将图片二进制数据写进入
                    handler.write(img_data)
                #重新打开这个文件并读取进行base64编码
                with open(loc, 'rb') as f:
                    image = base64.b64encode(f.read())
                    #将编码后的转换为utf-8以便于json格式调用SDK
                    image=str(image,'UTF-8')
                #调用SDK的人脸识别检测
                #登陆我的应用
                APP_ID = '22799939'
                API_KEY = 'f6WsuE34pzZl0qZbsWGmGu3M'
                SECRET_KEY = 'clOeRCxf2SA8PYSib9rWIdPrWNx2plwU'
                client = AipFace(APP_ID, API_KEY, SECRET_KEY)
                """选择图片类型"""
                imageType = "BASE64"
                """ 调用人脸检测 """
                client.detect(image, imageType);
                """ 如果有可选参数 """
                options = {}
                options["face_field"] = "age"
                options["max_face_num"] = 1
                options["face_type"] = "LIVE"
                options["liveness_control"] = "LOW"
                """ 带参数调用人脸检测 """
                #打印检测格式
                result = client.detect(image, imageType, options)#至此检测完成
                
                #建立一个字典，并且添加一些文件特有的数据至其中，转换成json格式
                #如果有人脸我们把它转移到一个特定的文件夹并标识这个人，如果没有识别出人脸，则删除这个图片
                if result["error_msg"] == 'SUCCESS':
                    dic = {}
                    dic["username"] = row[1].value
                    dic["id"] = row[0].value
                    dic["result"] = result["result"]
                    dic = json.dumps(dic)
                    print(dic)
                    with open('testadd.json','a+') as f:
                        f.write(dic+'\n')
# =============================================================================
#                    
#                     if not os.path.exists(dirs):
#                         os.makedirs(dirs)
#                         num = 1
#                     shutil.move(loc,dirs)
# =============================================================================
                else:
                    os.unlink(loc)


            
                
