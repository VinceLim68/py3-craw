#检验基价的准确性
import pandas as pd
import AJK,AjkCommPrice,MassController,LjCommPrice

import ToolsBox, Downloader, Outputer, ReqBuilder
import time, random, datetime,re
from urllib.parse import unquote


# 比较两个字符串的相似度方法1
from difflib import SequenceMatcher
def similarity(a, b):
    return SequenceMatcher(None, a, b).quick_ratio()
# print(similarity('CharlesCC', 'Charles'))0.875

# 比较两个字符串的相似度METHOD2
def similar(str1, str2):
    str1 = str1 + ' ' * (len(str2) - len(str1))
    str2 = str2 + ' ' * (len(str1) - len(str2))
    return sum(1 if i == j else 0
               for i, j in zip(str1, str2)) / float(len(str1))
# print(similar('CharlesCC', 'Charles'))

def mysimilar(a,b):
    str1 = a if len(a)>len(b) else b
    str2 = b if len(a)>len(b) else a
    # for item in str2:
    #     print(item in str1)
    return sum(1 if i in str1 else 0 for i in str2) / float(len(str2))


# str1="大唐世家(杏林)"
# str2="杏林大唐世家"
# print(similarity(str1,str2))
# print(similarity(str2,str1))
# print(mysimilar(str2,str1))
# print(mysimilar(str1,str2))


Ajk = AJK.AJK(AjkCommPrice.AjkCommPrice)
Ajk.headers = {
    "Request Method": "GET",
    "Status Code": "200 ",
    "Remote Address": "123.206.235.145:443",
    "Referrer Policy":"no-referrer-when-downgrade"
}

Lj = MassController.MassController(LjCommPrice.LjCommPrice)
Lj.headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Request Method": "GET",
    "Remote Address": "152.136.248.91:443",
    "Referrer Policy": "no-referrer-when-downgrade",
    "Host": "xm.lianjia.com"
}
community_name = " 大唐世家 "
ajkurl = ["https://xm.anjuke.com/community/?kw="+community_name]
ljurl=['https://xm.lianjia.com/xiaoqu/pg1rs'+community_name]

# Ajk.craw_controller(ajkurl,isComm=True)
Lj.craw_controller(ljurl,isComm=True)
