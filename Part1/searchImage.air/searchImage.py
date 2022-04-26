# -*- encoding=utf8 -*-
__author__ = "jiangsihui"

import os
import configparser
import time
import math
import urllib
import cv2
import numpy as np
from airtest.core.api import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from airtest_selenium.proxy import WebChrome
from selenium.webdriver import Chrome,ChromeOptions

auto_setup(__file__)

driver = WebChrome()
driver.implicitly_wait(20)

#author can't access to google due to it's banned in China, use baidu instead of google

url='https://image.baidu.com/'

#get file config.ini path and obtain the visit result number in configuration file
config = configparser.ConfigParser() 
path = os.path.abspath(".") + "/config.ini"
config.read(path,encoding="utf-8")
visit_result = int(config.get("ImageLocation","VISIT_RESULT")) - 1

#find the image by using config file value,use image lotus.jpg
driver.get(url)
driver.find_element_by_xpath("//img[@class='st_camera_off']").click()
driver.find_element_by_id("uploadImg").click()
driver.find_element_by_name("image").send_keys(os.path.abspath("./lotus.jpg"))
#result page is lazy loaded when visit_result > 30, we need to scroll page and make more images shows.
scroll_times = int(visit_result//30)
print(scroll_times)
if visit_result>30:
    for i in range(1,scroll_times+1):
        tempElement = driver.find_element_by_xpath("//a[@class='general-imgcol-item' and @data-index = '"+str(i*30-1)+"']")
        driver.execute_script("arguments[0].scrollIntoView()",tempElement)
#find the indication one     
print("//a[@class='general-imgcol-item' and @data-index = '"+str(visit_result)+"']")
imageElement = driver.find_element_by_xpath("//a[@class='general-imgcol-item' and @data-index ='"+str(visit_result)+"']//img")
driver.execute_script("arguments[0].scrollIntoView()",imageElement)
#store an screen shot of the last visited page, screenshot name should be timestamp+imageResult.jpg
timenow=str(int(time.time()))
#Requisite 1 in exercise part1,get current screenshot
driver.save_screenshot(timenow+"_screenResult.jpg")
#get image url for downloading
img_url = imageElement.get_attribute("src")
print(img_url)
request = urllib.request.Request(img_url)
response = urllib.request.urlopen(img_url)
#download the chosen picture
img = response.read()
imageName = str(timenow)+'_compareImage.jpg'
with open(imageName,'wb') as f:
    f.write(img)
#Compare search results are related to the used image, calculate simulitor %
#deal with source image
img1 = cv2.imread('lotus.jpg')
img1 = cv2.resize(img1,(8,8), interpolation=cv2.INTER_CUBIC)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img1_sum = np.sum(img1)
img1_mean = img1_sum / 64
img1_finger = np.where(img1 > img1_mean, 1, 0)

#deal with result image
img2 = cv2.imread(imageName)
img2 = cv2.resize(img2,(8,8), interpolation=cv2.INTER_CUBIC)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
img2_sum = np.sum(img2)
img2_mean = img2_sum / 64
img2_finger = np.where(img2 > img2_mean, 1, 0)

#Calculte simulator percent
isquel = img1_finger == img2_finger
index = isquel == True
han = isquel[index]
print(han)

hanming = len(han)
print('simulator%:{:.1%}'.format(hanming/64))

#Validate two images,if simulator percent is more than 0.9, Result image is the same as source image.
if hanming/64 >= 0.9:
    print("Result image is the same as source image.")
else:
    print("Result image is not the same as source image")



