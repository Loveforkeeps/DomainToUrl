#!/bin/python
# -*- coding=utf-8 -*-
#
# Author:EMo

import requests
import re
import io
import os
import sys
import math

# 默认获取Top500

if len(sys.argv) == 2:
    page = int(math.ceil(float(sys.argv[1])/20))
else:
    page = 25
        

url = "http://www.alexa.cn/siterank/"

pwd =  os.path.split(os.path.realpath(__file__))[0] + '/'

p = re.compile("【(.*?)】")

topdomains = list()

for i in range(1,page+1):
    listurl = url + str(i)

    with requests.get(listurl,timeout=10) as resp:
        topdomains.extend(re.findall(p,resp.content))


with io.open(pwd+'ChinaTop'+str(page*20)+'.txt','w',encoding='utf8') as f:
    for domain in topdomains:
        f.writelines(unicode(domain) + '\n')

print 'ok'