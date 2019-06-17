# coding:utf-8
import traceback
import datetime
import time
import re


def mylog(func):
    def _deco(*a, **b):
        try:
            # result = func(*a,**b) 
            # func(*a,**b)                  #以前只有return,但发现有返回值的函数加装饰器时，总是返回空，所以改成return func(*a,**b)
            return func(*a, **b)
            # return
        except Exception as e:
            # result = None
            with open('logtest.txt', 'a+') as fout:
                fout.write('\n               *******' + func.__name__ + '*******,error record by @mylog on ' + str(
                    datetime.datetime.now()) + '*************\n')
                traceback.print_exc(file=fout)
                print(traceback.format_exc())
                # return func
                # return result

    return _deco


def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        back = func(*args, **args2)
        print("@ %.3fs taken for {%s}\n" % (time.time() - t0, func.__name__))
        return back

    return newFunc


def pri(string):
    if len(string) % 2 != 0:
        string = string + ' '
    print(string)


def clearStr(string):
    # 清理字符串中的回车、空格等
    if isinstance(string, str):
        string = string.replace('<br/>', '').replace('\r', '').replace(' ', '').replace('\n', '').strip()
        string = string.replace(u'\xa0', '')  # 去除&nbsp;
        string = string.replace('<b>', '').replace('</b>', '')
        string = string.replace('<', '').replace('>', '')
        # 去除图形符号
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        string = co.sub(u'', string)
    return string


def ShowInvalideData(each_data):
    # temp = {}
    if each_data:
        if not each_data.has_key('total_floor'):  # 2016.6.1搜房网老是出现无效数据，进行判断，发现是别墅没有记载楼层信息造成的
            if u"别墅" in each_data['title']:
                each_data['total_floor'] = 4
                each_data['floor_index'] = 1
                each_data['spatial_arrangement'] = each_data['spatial_arrangement'] + u"别墅"
                # page_datas.append(each_data)
                print("没有总楼层,按照别墅填充！！！")
                for key, value in each_data.items(): print(" %s : %s" % (key, value))
                print("=" * 35)
                return True
            else:
                print("！！！没有总楼层！！！")
        elif not each_data.has_key('total_price'):
            print("！！！没有总价！！！")
        elif not each_data.has_key('area'):
            print("！！！没有面积！！！")
        elif not each_data.has_key('community_name'):
            print("！！！小区名！！！")
        printDic(each_data)
        print("=" * 35)
    return False


def confir(str):
    for i in range(0, 32):
        str = str.replace(chr(i), '')
    return str


def printDic(data):
    if isinstance(data, dict):
        for key in data:
            # key = to_str(key)
            # data[key] = to_str(data[key])
            print('%20s : %s' % (key, data[key]))
    else:
        # data = to_str(data)
        print(data)


def strToInt(string1):
    if isinstance(string1, str):
        b = re.findall(r'\d+\.?\d*', string1)
        # b = re.findall(r'\d+.\d+', string1)
        # print(b)
        try:
            # string1 = int(round(float(string1)))
            string1 = int(round(float(b[0])))
            # string1 =
            # string1 = int(round(float(re.sub("\D", "",string1))))
        # except ValueError as e:
        except:
            string1 = 0
    return string1


def priList(list_name, level=0):
    i = 1
    for yuansu in list_name:
        if isinstance(yuansu, list):  # 判断当前元素是不是列表
            priList(yuansu, level + 1)  # 如是,则递归调用,并且标记当前元素是列表
        else:
            for tab in range(level):  # 固定次数
                print("\t", end='')
            printDic(yuansu)
            print('************************  {0}  *************************'.format(i))
            i += 1


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str

def clear_comm(str):
    #清除小区名称中（）内的部分
    return str.split('(')[0].split('（')[0].strip()

#
# str2 = '全厦门 吉🏠诚意出售，仅此一套！'
# a = strToInt(str2)
# print(clearStr(str2))
# if isinstance(str2,str):
#     print(clearStr(str2))
# print(clear_comm(str2))

