# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 15:44:00 2018

@author: 小康
"""

import requests
from bs4 import BeautifulSoup
import time
from lxml import etree
import re 
import pymongo
import os

def get_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    return soup
def get_links(link_url):
    soup = get_page(link_url)
    links_div = soup.find_all('li')
    links = [div.a.get('href') for div in links_div]
    del links[0:7]
    return links

def test(url):
    response = requests.get(url)
    html = etree.HTML(response.text)
    result = etree.tostring(html)
    mm = result.decode('utf-8')
    kk = etree.HTML(mm)
    results = kk.xpath('//div[@class="pagenavi"]/a//text()')[-2]
    print(results)
    for result1 in range(1,int(results)+1):       
            new_url = url+'/{}'.format(result1)
            response = requests.get(new_url)
            pattern = re.compile('<img src="(h.*?)" alt')
            title = re.compile('<img src=".*" alt="(.*?)"')
            title1 = re.findall(title,response.text)[0]
            pic_jpg = re.findall(pattern,response.text)[0]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 \
           Safari/537.36 Edge/17.17134'} #声明一个请求头
            headers['Referer'] = 'http://www.mzitu.com/'
            img = requests.get(pic_jpg,headers=headers)
            path = 'D:\MEIZI\{}'.format(title1)
            isExists = os.path.exists(path)
            if isExists: 
                os.chdir(path)                
            else:
                os.makedirs(path) 
                os.chdir(path)                           
            name = pic_jpg[-9:-4]
            with open(name + '.jpg','wb+') as f:
                f.write(img.content)
            pic = {
                'id':title1,
                'title':result1,
                'pic_jpg':pic_jpg}
            save_to_mongo(pic)

def save_to_mongo(pic):
    try:
        if db[MONGO_COLLECTION].insert(pic):
            print('存储成功')
    except Exception:
        print('存储失败')

MONGO_URL = 'localhost'
MONGO_DB = 'meizitu'
MONGO_COLLECTION = 'Album'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

url = ''  #输入 http://www.mzitu.com

links = get_links(url)
for link in links[0:2]:
    time.sleep(2)
    print(link)
    a = test(link)
