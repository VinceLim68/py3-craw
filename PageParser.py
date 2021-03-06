from bs4 import BeautifulSoup
import re
import datetime
import traceback
import MatchID,ToolsBox
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


class PageParser(object):

    def __init__(self):
        self.MI = MatchID.MatchID()
    #     self.r1 = re.compile(r"(\d+\.?\d*)(.*)")             #正则：数字+单位
    #     self.r2 = re.compile(r"(\d+).*")                     #正则：取字符串中的数字

    def parse_urls(self , soup):
        pass

    def parse_datas(self,soup):
        pass

    def is_check(self,soup):
        return False

    def get_soup(self,html,parser_build = 'lxml'):
        # 根据不同的解析器得到soup
        # parser_build:解析器------->html.parser,lxml
        return BeautifulSoup(html,parser_build)

    def page_parse(self,html_cont,parser_build = 'lxml'):
        # 解析网页的主模块
        if html_cont == 404:
            print('出现请求错误，返加4XX错误，可能被服务器禁止访问')
            new_urls = new_datas = html_cont
        else:
            soup = self.get_soup(html_cont,parser_build)

            #在这里加上辨识是否有验证码的代码
            if self.is_check(soup):
                new_urls = new_datas = 'checkcode'
            else:
                new_urls = self.parse_urls(soup)
                new_datas = self.parse_datas(soup)
                # ToolsBox.priList(new_datas)
                # print("?"*50)
        return new_urls,new_datas

    def parse_floor(self,item,pattern = None):
        '''
        高层/(共30层)-->拆成楼层和总层数,        安居客、链家中使用
        传入：        item-->字符串        sep-->分隔符
        '''
        # 修改整个模块，应对“高层/(共30层)1室1厅”的情况
        # 低楼层共20层3室2厅
        # split1 = '[）,\)]+'       #第一次拆分，把相连的‘1室1室’之类的拆掉
        # split2 = '[\(,（,\/]'        #第二次拆分，把楼层和总层分开
        # try:
        #     a = re.split(split1, item)
        #     b = re.split(split2, a[0])
        #     # print(a)
        #     if re.search(split2, a[0]):
        #         total_string = b[1]
        #         index = b[0]
        #     else:
        #         total_string = b[0]
        #         index = ''
        #     # input(total_string)
        #     # input(index)
        #     total_floor = int(re.sub("\D", "", total_string))
        #     if u"高" in index:
        #         floor_index = int(total_floor * 5 / 6)
        #     elif u"低" in index:
        #         floor_index = int(total_floor / 6)
        #     else:
        #         floor_index = int(total_floor / 2)

        # 修改可兼容“低楼层共20层3室2厅”这种不带分割符的情况
        try:
            if pattern is None : pattern = '((?P<floor>[高中低])楼?层)?.?共?(?P<total>\d+)层'
            temp_str = re.search(pattern, item, flags=0).groupdict()
            # print(temp_str)
            total = int(temp_str['total'])
            if temp_str['floor']:
                if u"高" in temp_str['floor']:
                    floor = int(total * 5 / 6)
                elif u"低" in temp_str['floor']:
                    floor = int(total / 6)
                else:
                    floor = int(total / 2)
            else:
                floor = 1
        except Exception as e:
            with open('logtest.txt','a+') as fout:
                fout.write('\n******' + str(datetime.datetime.now()) + ' *********Erro in parse_floor*************\n')
                fout.write('Parse Failt of :%s \n'%item.encode('utf8'))
                traceback.print_exc(file=fout)
                print (traceback.format_exc())
        # print(item)
        return floor,total

    def parse_item(self,string):
        # 2016.8.17增加：传入一个字符串，用正则判断它是面积？户型？单价？楼层？建成年份？优势？解析后返回一个键对值
        try:
            string = string.decode('utf8').strip()
        except:
            string = string.strip()

        parse_dict = {}

        r1_1 = '(\d+)平方米'
        r1_2 = '(\d+.?\d+)平米'        #厦门house的面积是浮点数
        r1_3 = '(\d+.?\d+)㎡'         #2016.9.13增加麦田的面积解析
        r1_4 = '(\d+.?\d+)m²'        #2017.3.8安居客
        r1_5 = '(\d+.?\d+)�O'        #2018.8.3搜房,这个乱码就是㎡
        r1_6 = '(\d+.?\d+)平'        #2018.8.3搜房,这个乱码就是㎡
        r2_1 = '\d+室'
        r2_2 = '\d+房'
        r3_1 = '(\d+)元/'
        r3_2 = '(\d+)万'
        r4 = '\d+层'
        r4_1 = '((?P<floor>[高中低])楼?层)?.?共?(?P<total>\d+)层'
        r5_1 = '(\d{4})年'
        r5_2 = '年.*(\d{4})'

        if re.search(r1_1, string, flags=0)\
            or re.search(r1_2, string, flags=0)\
            or re.search(r1_3, string, flags=0)\
            or re.search(r1_4, string, flags=0)\
            or re.search(r1_5, string, flags=0)\
            or re.search(r1_6, string, flags=0)\
            or re.search(r2_1, string, flags=0)\
            or re.search(r2_2, string, flags=0)\
            or re.search(r3_1, string, flags=0)\
            or re.search(r3_2, string, flags=0)\
            or re.search(r4, string, flags=0)\
            or re.search(r5_1, string, flags=0)\
            or re.search(r5_2, string, flags=0):

            if re.search(r1_1, string, flags=0):
                parse_dict['area'] = int(re.search(r1_1, string).groups(0)[0])
            elif re.search(r1_2, string, flags=0):
                parse_dict['area'] = int(round(float(re.search(r1_2, string).groups(0)[0]),0))
            elif re.search(r1_3, string, flags=0):                                          #2016.9.13增加麦田的面积解析
                parse_dict['area'] = int(round(float(re.search(r1_3, string).groups(0)[0]),0))
            elif re.search(r1_4, string, flags=0):                                          #2017.3.8安居客的面积解析
                parse_dict['area'] = int(round(float(re.search(r1_4, string).groups(0)[0]),0))
            elif re.search(r1_5, string, flags=0):  # 2018.8.3搜房的面积解析
                parse_dict['area'] = int(round(float(re.search(r1_5, string).groups(0)[0]), 0))
            elif re.search(r1_6, string, flags=0):  # 2019.9.9乐居的面积解析
                parse_dict['area'] = int(round(float(re.search(r1_6, string).groups(0)[0]), 0))
            else:
                pass

            # if re.search(r4, string, flags=0):
            #     parse_dict['floor_index'],parse_dict['total_floor'] = self.parse_floor(string)

            if re.search(r4_1, string, flags=0):
                parse_dict['floor_index'], parse_dict['total_floor'] = self.parse_floor(string,r4_1)
                # temp_str = re.search(r4_1, string, flags=0).groupdict()
                # # print(temp_str)
                # parse_dict['total_floor'] = int(temp_str['total'])
                # if temp_str['floor']:
                #     if u"高" in temp_str['floor']:
                #         parse_dict['floor_index'] = int(parse_dict['total_floor'] * 5 / 6)
                #     elif u"低" in temp_str['floor']:
                #         parse_dict['floor_index'] = int(parse_dict['total_floor'] / 6)
                #     else:
                #         parse_dict['floor_index'] = int(parse_dict['total_floor'] / 2)
                # else:
                #     parse_dict['floor_index'] = 1
                # print(temp_str.group(0))
                # parse_dict['floor_index'] = floor_index
                # print(temp_str)
                # string = re.sub(r4_1, "", string, count=0, flags=0)
                string = ToolsBox.clearStr(re.sub(r4_1, "", string, count=0, flags=0))
                # print(string)

            if re.search(r2_1, string, flags=0) \
                    or re.search(r2_2, string, flags=0):
                parse_dict['spatial_arrangement'] = string.strip()


            if re.search(r5_1, string, flags=0):
                parse_dict['builded_year'] = int(re.search(r5_1, string).groups(0)[0])
            elif re.search(r5_2, string, flags=0):
                parse_dict['builded_year'] = int(re.search(r5_2, string).groups(0)[0])
            else:
                pass
        else:
            if string == '|' or string == '|':
                pass
            elif string == '':
                pass
            else:                           #re.search('[南北东西]', string, flags=0):
                parse_dict['advantage'] = string.strip()
        # print(parse_dict)
        return parse_dict

    def excep(self,str):
        # 去除不需要的小区
        ex = ['厦门周边', '漳州', '泉州', '龙岩', '长泰',
              '角美', '漳州港', '南安', '晋江','厦门后花园','厦门西']
        flag = False
        for item in ex:
            if item in str:
                flag = True
                break
        return flag

    def add_advantage(self,d1,each_data):
        # 合并advantage,d1是刚解析出的字段，d2是ecah_data
        if len(d1) > 0:
            if ('advantage' in each_data.keys()) \
                    and ('advantage' in d1.keys()) \
                    and (each_data['advantage'] != ''):
                each_data['advantage'] = each_data['advantage'] + ',' + d1['advantage']
            else:
                each_data = dict(each_data, **d1)
        # if ('advantage' in each_data.keys()) and ('advantage' in d1.keys()):
        #     d1['advantage'] = each_data['advantage'] + ',' + d1['advantage']
        return each_data

    def pipe(self,datadic):
        # 有效性检验
        # 把小区的区块、板块及小区地址写到title里去
        for key in datadic:
            datadic[key] = ToolsBox.clearStr(datadic[key])

        title_temp = ''
        if 'region' in datadic.keys():
            if self.excep(datadic['region'].strip()):
                return False
            else:
                title_temp += ' r:' + datadic['region'].strip()

        if 'block' in datadic.keys():
            if self.excep(datadic['block'].strip()):
                return False
            else:
                title_temp += ' b:' + datadic['block'].strip()
        if 'community_address' in datadic.keys():
            datadic['community_address'] = datadic['community_address'].strip()
            title_temp += ' a:' + datadic['community_address'].strip()
        if 'title' in datadic.keys():
            title2 = title_temp.strip() + ' ' + datadic['title']
        else:
            title2 = title_temp.strip()
        if len(title2) > 50 :
            title2 = title2[:50]
        datadic['title'] = title2.strip()

        if ('community_name' not in datadic.keys()) or len(datadic['community_name'])<2:
            return False

        datadic['community_id'] = self.MI.matchid(datadic)
        if ('total_floor' in datadic.keys()) and ('total_price' in datadic.keys()) and ('area' in datadic.keys()) :
            if datadic['total_price'] is None or datadic['area'] is None or datadic['area'] == 0:
                return False
            else:
                datadic['price'] = round(float(datadic['total_price'] * 10000 / datadic['area']), 2)
            if datadic['price'] < 1500 or datadic['price'] > 300000:
                return False

            # if datadic['community_name'] is None or len(datadic['community_name'])<2:
            #     return False
            if datadic['total_floor'] > 60:
                datadic['total_floor'] = 35         #把过高楼层的设为35层
            if datadic['total_price'] == 0 : return False                       #2016.9.13 价格为0的过滤掉

            if 'builded_year' in datadic.keys():
                if datadic['builded_year'] < 1900: datadic['builded_year'] = 0

            if datadic['area'] > 20000: return False        #面积过大，有时是填写错误，而且面积大于20000的价格参考意义也不大，舍弃
            if 'price' not in datadic.keys(): return False       #2016.8.1 有时解析过程中出错，跳过了price字段解析，造成没有price,舍弃

            #2017.4.14 detail_url字段太长，处理一下
            if len(datadic['details_url']) > 250:datadic['details_url'] = datadic['details_url'][:249]
            if 'advantage' in datadic.keys():
                if len(datadic['advantage']) > 20:datadic['advantage'] = datadic['advantage'][:20]
            return datadic
        else:
            if not ('total_floor' in datadic.keys()) and ('total_price' in datadic.keys()) and ('area' in datadic.keys()) and ('community_name' in datadic.keys())  :
                if u"别墅" in datadic['title']:
                    if datadic['total_price'] is None or datadic['area'] is None or datadic['area'] == 0:
                        return False
                    else:
                        datadic['price'] = round(float(datadic['total_price'] * 10000 / datadic['area']), 2)
                    datadic['total_floor'] = 4
                    datadic['floor_index'] = 1
                    datadic['spatial_arrangement'] = datadic['spatial_arrangement'] + u"别墅" if 'spatial_arrangement' in datadic.keys() else u"别墅"
                    return datadic
            return False
        
if __name__=="__main__":

    # url = 'http://xm.ganji.comhttp://aozdclick.ganji.com/gjadJump?gjadType=3&target=pZwY0jCfsL6VshI6UhGGshPfUiqhmyOMPitzPWDvn1E1nHDYXaOCIAYhuj6-n176mhNVuAm1niYYP1FhsH91rjnVP1I6nAcYuHnvPynzFWDkPjmQPHDOPWchnHEOnH03rj9zPW9vPH93FWcvnHm1PjnQnHEhP1utsgkVFWItnW7tsgkVFW0LPjmQmWmLsH9QnvEVPj6BnaY3rjmQsyELP1DLnAP6rymQuamQPjbznjmYn1mzP1DdFhIJUA-1IZGbFWDh0A7zmyYhnau8IyQ_FWEhnHDLsWcOsWDvnz3QPjchUMR_UamQFhOdUAkhUMR_UT&end=end'
    # print(len(url) )


    str2 = "高楼层(共6层)1室1厅"
    str2 = "低层(共34层)"
    # str2 = "低楼层共20层3室2厅"
    # str2 = "1室1厅"
    # str2 = "中楼层/31层"
    #
    p = PageParser()
    example = p.parse_item(str2)
    print(example)
    # flag = p.excep('厦门周边')
    # print(flag)
    # print(p.excep('湖里大道′))
    # print str[0:3] #截取第一位到第三位的字符
    # parser = HtmlParser()
    # # str1 ='4层2008年建'
    # str1 = '中楼层(共10层)2006年建塔楼'
    # if ')' not in str1:
    # #     split = ')'
    # # else:
    #     str1 = str1.replace('层', '层)')
    #     print str1
    #     # index = str1.index() + 1
    #     # # str1 = str1(0:index)
    #     # print str1[0:index]+')'+str1[index:]+' '

    # # str1 ='4层'
    # # a = (parser.parse_item(str1))
    # for item in str1.split(')'):     #2017.4.1链家格式有改
    # # for i in range(0,len(position)-2):
    #     d1 = {}
    #     # d1 = self.parse_item(position[i].strip())
    #     d1 = parser.parse_item(item.strip())          #2017.4.1链家格式有改
    #     print(d1)
        # each_data = dict(each_data, **d1)
    # print a



