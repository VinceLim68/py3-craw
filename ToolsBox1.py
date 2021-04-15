# coding:utf-8
import traceback
import datetime
import time
import re
import pymysql


# 统一拿连接数据库的实例，以后有修改就可以一次改完
def get_database() -> object:
    """

    :rtype: object
    """
    return pymysql.connect(host='localhost', user="root", passwd="root", db="property_info", charset="utf8", port=3306)


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
    # 清除小区名称中（）内的部分
    return str.split('(')[0].split('（')[0].strip()


# 把中文字符串转成阿拉伯数字
# constants for chinese_to_arabic
CN_NUM = {
    '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
}

CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}


def chinese_to_arabic(cn: str) -> int:
    unit = 0  # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val


# TODO: make a full unittest
def test():
    test_dig = ['八八八',
                '28之一十一',
                '一百二十三',
                '一千二百零三',
                '一万一千一百零一',
                '十万零三千六百零九',
                '一百二十三万四千五百六十七',
                '一千一百二十三万四千五百六十七',
                '一亿一千一百二十三万四千五百六十七',
                '一百零二亿五千零一万零一千零三十八']
    for cn in test_dig:
        x = chinese_to_arabic(cn)
        # print(cn, x)
    assert x == 10250011038


def Break_up_the_address(address):
    # regex = "(?P<province>[^省]+自治区|.*?省|.*?行政区)?" \
    # + "(?P<city>[^市]+自治州|.+?地区|.+?行政单位|.+?盟|.+?市辖区|.*?市)?"\
    # + "(?P<county>[^县]+县|.*?县|.*?区|.+?旗|.+?海域|.+?岛)?"\
    # + "(?P<town>[^镇]+镇|.*?街道|.*?镇|.*?乡)?"\
    # + "(?P<village>[^村]+村|.*?村|.*?路|.*?街|.*?弄|.*?园|.*?中心|.*?里|.*?寺|.*?苑|.*?段|.*?厝|.*?居委会|.*?办事处|.*?街办|.*?街道办|.*?街口|.*?巷|.*?条|.*?道|.*?场|.*?矿|.*?区)?"\
    # + "(?P<loudong>[^号]+号|.*?号|.*?号院)?"\
    # + "(?P<qi>[^期]+期|.*?期|.*?区)?"\
    # + "(?P<dong>[^幢]+幢|.*?楼|.*?幢|.*?栋|.*?座|.*?梯|.*?门)?"\
    # + "(?P<danyuan>[^单元]+单元|.*?单元)?"\
    # + "(?P<ceng>[^室]+室|.*?室|.*?房|.*?号|.*)";
    if re.search('([a-zA-Z0-9一二三四五六七八九十东西南北中]+[区期])+', address):
        regex = "(?P<province>[^省]+自治区|.*?省|.*?行政区)?" \
                + "(?P<city>[^市]+自治州|.+?地区|.+?行政单位|.+?盟|.+?市辖区|.*?市)?" \
                + "(?P<county>[^县]+县|.*?县|.*?区|.+?旗|.+?海域|.+?岛)?" \
                + "(?P<town>[^镇]+镇|.*?街道|.*?镇|.*?乡)?" \
                + "(?P<village>[^村]+村|.*?村|.*?路|.*?街口|.*?街|.*?弄|.*?条|.*?大道|\
                .*?里|.*?居委会|.*?办事处|.*?巷|.*?道|.*?段|.*?街办|.*?街道办|\
                .*?中心|.*?寺|.*?园|.*?苑|.*?厝|.*?场|.*?矿|.*?区)" \
                + "(?P<buildingnumber>\d+号院|\d+号)?" \
                + "(?P<com>([\u4e00-\u9fa5])+)" \
                + "(?P<qi>([a-zA-Z0-9一二三四五六七八九十东西南北中]+[区期]))+" \
                + "(?P<dong>[a-zA-Z0-9一二三四五六七八九十#]+[幢楼栋座梯门])?" \
                + "(?P<danyuan>[a-zA-Z0-9一二三四五六七八九十#]+单元)?" \
                + "(?P<ceng>[a-zA-Z0-9一二三四五六七八九十#]+[室房号])?"

    else:
        regex = "(?P<province>[^省]+自治区|.*?省|.*?行政区)?" \
                + "(?P<city>[^市]+自治州|.+?地区|.+?行政单位|.+?盟|.+?市辖区|.*?市)?" \
                + "(?P<county>[^县]+县|.*?县|.*?区|.+?旗|.+?海域|.+?岛)?" \
                + "(?P<town>[^镇]+镇|.*?街道|.*?镇|.*?乡)?" \
                + "(?P<village>[^村]+村|.*?村|.*?路|.*?街口|.*?街|.*?弄|.*?条|.*?大道|\
                .*?里|.*?居委会|.*?办事处|.*?巷|.*?道|.*?段|.*?街办|.*?街道办|\
                .*?中心|.*?寺|.*?园|.*?苑|.*?厝|.*?场|.*?矿|.*?区)" \
                + "(?P<buildingnumber>\d+号院|\d+号)?" \
                + "(?P<com>[\u4e00-\u9fa5]+)" \
                + "(?P<qi>([a-zA-Z0-9一二三四五六七八九十东西南北中]+[区期]))?" \
                + "(?P<dong>[a-zA-Z0-9一二三四五六七八九十#]+[幢楼栋座梯门])?" \
                + "(?P<danyuan>[a-zA-Z0-9一二三四五六七八九十#]+单元)?" \
                + "(?P<ceng>[a-zA-Z0-9一二三四五六七八九十#]+[室房号])?"
    pattern = re.compile(regex)
    match = re.search(pattern, address)
    print(regex)
    if match:
        print(match.groupdict())

#
# Break_up_the_address('城内路二巷76号')
# Break_up_the_address('仓山区对湖街道首山街口23号院米兰春天2#楼104单元')
# str2 = '后江埭路46号之7'
# a = strToInt(str2)
# print(a)
# print(clearStr(str2))
# if isinstance(str2,str):
#     print(clearStr(str2))
# print(clear_comm(str2))
