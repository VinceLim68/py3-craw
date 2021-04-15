"""
@project:利用地址获取对应小区，以最抓取距离最近的五个小区
@author:Giserlei
@file:地址_小区.py
@环境：python3.6、Pycharm
@time:2021-04-02

"""


import json
from urllib.request import urlopen, quote
import requests
import pandas as pd
import numpy as np
import datetime
import time
from fake_useragent import UserAgent
from w3lib.http import basic_auth_header

''' 快代理隧道代理设置 '''
username = "t10490816493919"

password = "r7vro728"

bah = basic_auth_header(username, password)

proxy_ip = 'tps198.kdlapi.com:15818'

proxy_get = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
}


# ua = UserAgent()
#
# ua_get = ua.random
#
# header_get = {
#     'User-Agent': ua_get,
#     'Connection':"close"
# }

# 获取经纬度
def getlnglat(address):
    ua = UserAgent()

    ua_get = ua.random

    header_get = {
        'User-Agent': ua_get,
        'Connection': "close"
    }

    url = 'http://api.map.baidu.com/geocoding/v3/?address='
    output = 'json'
    ak = "6p9Rmy7jmL0iuEzUVvySwEVO6xuYA1h7"
    # 通过百度创建应用得到ak，记得写为浏览器端，然后写*
    address = quote(address)
    uri = url + address + '&output=' + output + "&ak=" + ak
    try:
        req = requests.get(uri, headers=header_get).text
        #         print( req)

        # res = req.read().decode()
        time.sleep(0.1)
        # print(res)
        temp = json.loads(req)
        if temp['status'] == 0:

            lat = temp['result']['location']['lat']
            lng = temp['result']['location']['lng']

            #  百度地图解析结果精度判断以字段comprehension的值为依据
            acc = temp['result']['comprehension']
            use = temp['result']['level']
        else:
            lat = 0
            lng = 0
            acc = "无"
            use = '无'
        # return lat, lng,acc
        return str(lat) + ',' + str(lng)


    except Exception as e:
        print(e)
        #         print(data['地址1'].iloc[i])
        time.sleep(3)
        getlnglat(address)
# 进度条
# def process_bar(percent, start_str='', end_str='', total_length=0):
#     bar = ''.join(["\033[31m%s\033[0m"%'   '] * int(percent * total_length)) + ''
#     bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent*100) + end_str
#     print(bar, end='', flush=True)

def get_jwd(num):
    jwd = []
    print('正在解析地址坐标')
    for i in range(num):
        time.sleep(0.1)
        end_str = '100%'
        # process_bar(i / (shuju - 1), start_str='', end_str=end_str, total_length=15)
        a = getlnglat(data['地址'].iloc[i])
        #     print(a)
        jwd.append(a)
    return  jwd


class  get_address_com:
    xqmmingz = []
    Sec_pois_list = pd.DataFrame()
    def __init__(self,xq_name,position,leng,outpath):
    # 第三个函数利用列表循环读取每个小区的指数信息
    #     xqmmingz = []
    #
    #
    #     Sec_pois_list = pd.DataFrame()
        self.xq_name = xq_name
        self.position = position
        self.leng = leng
        self.outpath=outpath

    def create_json(self,url):
        #     js = requests.get(url, proxies=proxies).text
        js = requests.get(url).text
        json_dict = json.loads(js)
        #     url_file =urlopen(url)
        #     json_file = url_file.read()
        #     json_dict = json.loads(json_file)
        return json_dict

    # 解析Josn数据，并返回为List
    def read_json(self,json_dict):
        name1 = []
        address1 = []
        city1 = []
        area1 = []
        location1 = []
        distance1 = []
        tag1 = []
        # 依次读取Json数据，保存到List中
        for i in json_dict["results"]:
            name = i['name']
            name1.append(name)
            address = i['address']
            address1.append(address)
            city = i['city']
            city1.append(city)
            area = i['area']
            area1.append(area)
            location = i['location']
            location1.append(location)
            distance = i['detail_info']['distance']
            distance1.append(distance)
            tag = i['detail_info'].get('tag', 0)
            tag1.append(tag)

        c = {"name": name1, "address": address1, "ncity": city1, "area": area1, "location": location1,
             "distance": distance1, "tag": tag1}
        c = pd.DataFrame(c)
        return c


    def get_my_want(self):
        for i in range(0, leng):

            print("地址:" + xq_name[i] + "  对应小区数据正在采集剩余  " + str(leng - i) + "个地址待采集")
            try:
                # for i in range(0,12):
                key_word = quote('小区')
                coordinate = position[i]
                radius = 500
                page_name = 0
                ak = "UlAhxvqsGWq7KEEBMOpqLnsFNfbSbIcA"
                page_size = 5
                filter1 = "sort_name:distance|sort_rule:1"

                ur = "http://api.map.baidu.com/place/v2/search?query=" + str(
                    key_word) + "&location=" + coordinate + "&scope=2" + "&filter=sort_name:distance|sort_rule:1" \
                                                                         "&radius=" + str(
                    radius) + "&output=json" + "&page_size=" + str(page_size) + "&ak=" + "UlAhxvqsGWq7KEEBMOpqLnsFNfbSbIcA"
                a = self.create_json(ur)
                self.Sec_pois_list = self.Sec_pois_list.append(self.read_json(a))
                lang = len(self.read_json(a))

                self.xqmmingz.extend([xq_name[i] for x in range(0, lang)])
                self.Sec_pois_list['原小区地址'] = self.xqmmingz

                self.Sec_pois_list.to_excel(self.outpath)
            except(KeyError):
                print("继续")

if __name__ == '__main__':

    data = pd.read_excel('G:\\郑磊工作交接\\test.xlsx')
    # 获取所有的小区经纬
    shuju = len(data['地址'])
    data['经纬度']=get_jwd(shuju)
    print('正在解析地址坐标')
    xq_name = data['地址']
    position = data['经纬度']
    output='G:\\郑磊工作交接\\test_rest.xlsx'
    leng = len(data)
    get_com=get_address_com(xq_name,position,leng ,output)
    get_com.get_my_want()