# -*- encoding=utf8 -*-
__author__ = "jiangsihui"

from airtest.core.api import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from airtest_selenium.proxy import WebChrome

auto_setup(__file__)

driver = WebChrome()
driver.implicitly_wait(20)
"""
author can't access to google due to it's banned in China, use baidu instead of google
"""
url='https://image.baidu.com/'
VISIT_RESULT=3

driver.get(url)
driver.find_element_by_xpath("//img[@class='st_camera_off']").click()
driver.find_element_by_id("uploadImg").click()
driver.find_element_by_name("image").send_keys(os.path.abspath("./lotus.jpeg"))
s = driver.find_element_by_xpath("(((//div[@class='graph-similar-list']//div[@class='general-imgcol'])[3])//img)[1]").get_attribute("src")
print(s)


