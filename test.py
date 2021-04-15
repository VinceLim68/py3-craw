import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import ToolsBox,re
from urllib.parse import quote,unquote

#设置中文字体
# myfont = FontProperties(fname='C:/Windows/Fonts/STKAITI.TTF')
#
# A = np.array([[0, 1, 1, 0, 0],[1, 1, 0, 0, 1]]) #原空间
# B = np.array([[3,0],[0,2]])     #线性变换矩阵
# Y = np.dot(B,A)
#
# plt.clf()
# plt.plot(A[0],A[1],'-*',lw=2)
# plt.text(0.6,1.03,u'变换前',fontsize =14,fontproperties=myfont)
# plt.plot(Y[0],Y[1],'-r*',lw=2)
# #font size: xx-small;x-small;small;medium;large;x-large;xx-large
# plt.text(0.6,2.03,u'变换后',fontsize ='large',fontproperties=myfont)
# plt.axis([0,3,0,3]);plt.grid(True)
# plt.show()

# A = np.array([[0, 1, 1, 0, 0],[1, 1, 0, 0, 1]]) #原空间
#
# plt.clf()
# B1=np.array([[1,0],[1,1]])
# B2=np.array([[1,0],[-1,1]])
# B3=np.array([[1,1],[0,1]])
# B4=np.array([[1,-1],[0,1]])
#
# Y1 = np.dot(B1,A)
# Y2 = np.dot(B2,A)
# Y3 = np.dot(B3,A)
# Y4 = np.dot(B4,A)
#
# plt.subplot(221)
# plt.plot(A[0],A[1],'-*',lw=2)
# plt.plot(Y1[0],Y1[1],'-r*',lw=2)
# plt.axis([-1,3,-1,3]);plt.grid(True)
# plt.subplot(222)
# plt.plot(A[0],A[1],'-*',lw=2)
# plt.plot(Y2[0],Y2[1],'-r*',lw=2)
# plt.axis([-1,3,-1,3]);plt.grid(True)
# plt.subplot(223)
# plt.plot(A[0],A[1],'-*',lw=2)
# plt.plot(Y3[0],Y3[1],'-r*',lw=2)
# plt.axis([-1,3,-1,3]);plt.grid(True)
# plt.subplot(224)
# plt.plot(A[0],A[1],'-*',lw=2)
# plt.plot(Y4[0],Y4[1],'-r*',lw=2)
# plt.axis([-1,3,-1,3]);plt.grid(True)
# plt.show()
# new_url = '844242'
# print(new_url)
# match_comm = re.findall(r'^\d+$', new_url)
# print(new_url)
# print(match_comm)
# ToolsBox.printDic(match_comm)
# print(unquote(match_comm[0],'utf-8')=='安全局宿舍')
# # print(len(match_comm)==1)
# string = '共6层'
# # string = '7/15层'
# # string = '12层     1室1厅'
#
# split1='[）,\),\s]+'
# split2='[\(,（,\/]'
# # a =string.split('|').split(' ')
# # a = re.split(r'[\(,\/,|,（,）,\),\s]+',string)
# a = re.split(split1,string)
# b = re.split(split2,a[0])
# print(a)
# print(b)
# if re.search(split2,a[0]):
#     total_string = b[1]
#     index = b[0]
# else:
#     total_string = b[0]
#     index = ''
# total_floor = int(re.sub("\D", "", total_string))
# if u"高" in index:
#     floor_index = int(total_floor*5/6)
# elif u"低" in index:
#     floor_index = int(total_floor/6)
# else:
#     floor_index = int(total_floor/2)
# print(floor_index)
# print(total_floor)
# after_sep = (item.split(sep)[1]) if sep in item else item
#             # print(after_sep)
# get_num = re.sub("\D", "", after_sep)
#
# total_floor = int(get_num)
# index = item.split(sep)[0] if sep in item else " "

# a = re.split(r'\s*[|,\s]\s*',string)
# print(a[0])
# dic = {}
# r2_1 = '\d+室'
# r2_2 = '\d+房'
# r3_1 = '(\d+)元/'
# r3_2 = '(\d+)万'
# r4 = '\d+层'
# # if re.search(r4, string, flags=0) and ')' in string:
# #     print(string.split(')'))
#     # re.split(")", string)
# dic['a'] = 5
# listtest = dic
# dic['b'] = 8
# listtest = dic
# print(listtest)
#
# import pymysql
# db = pymysql.connect(host ='localhost', user ="root", passwd ="root", db ="property_info", charset ="utf8", port = 3306)
# db = ToolsBox.get_database()
# print(db)
# print(f'{6:^30}')
# # print('\n'.join([' '.join([f'{i}*{j}={i*j:2d}' for j in range(1,i+1)]) for i in range(1,10)]))
# import pygame
# path = r'C:\Users\Administrator\Desktop\sound_test.wav'
# #初始化音频
# pygame.mixer.init()
# #加载路径文件
# pygame.mixer.music.load(path)
# #播放
# pygame.mixer.music.play()
# #停止播放
# pygame.mixer.music.stop()
# #代码运行后持续300秒

# 单独匹配小区id的测试程序
import MatchID
# matchid = MatchID.MatchID()
# # print(matchid.comm_arr)
# add = { 'title': 'r:同安-城北二手房 a:汀溪街 降价出售，江头公园旁，嘉禾路，国泰大厦，精装4房，电梯中层', 'community_name': '大唐水云间'}
# # commid = matchid.matchid(add)
# # print('2'*40)
# # print(commid)
# getid = matchid.get_id_from_arr(add, matchid.comm_arr)
# print('get id from arr is %s'%getid)
# id = matchid.handle_match_mul(add,getid)
# print(id)

from fake_useragent import UserAgent
# ua = UserAgent()
# print(ua.random)

# var1 = []
# var2 = [1,2,3]
# var1.append(var2)
#
# var3=[3,3,3]
# var1.append(var3)
# print(var1)
# var1[0]=var3
# print(var1)
#
# def get_add_com_similar(self, add1: str, add2: str = ""):
    # 把地址拆成路和号分别比较
# regex = "(?P<road>.+?路|.+?道|.+?街|.+?巷|.+?road|.+?线|.+?段|.+?里|.+?弄|.+?条|.+?出口|.+?入口|.+?高速|.+?快速|.+?胡同)" \
#                 "(?P<road_number>([a-zA-Z0-9一二三四五六七八九十百千甲之乙丙丁支-]+(弄|号院|号)(?!楼))+)"
#
# add1 = "宝圣东路一巷127号"
# add1 = "合阳大道宝龙城市花园"
# add1 = "桃源南路2号附24号"
# add1 = "鱼嘴镇和韵支路（堰坪湖旁）"
# add1 = "宝圣东路、靠近机场路"
# add1 = "前进街邦泰花园|江津区德感街道鼎康路55号"
# add1 = "空港大道63号（空港广场对面|中国银行旁）"
# add1list = re.search(regex, add1)
# if add1list :
#     print(add1list.groupdict())
# else:
#     print('no')
#
# r4_1 = '[高中低]楼层.?共\d+层'
# string = "低楼层共20层3室2厅"
# print(re.search(r4_1, '高楼层(共5层)3室1厅', flags=0))
# # str1 = re.search(r4_1,"", string, flags=0).group(0)
# string = re.sub(r4_1, "", string, count=0, flags=0)
# print(ToolsBox.clearStr(string))
# r = '[县镇区]$'
# str = '厦门区镇'
# string = re.sub(r, "", str, count=0, flags=0)
# print(string)
# input_file = "C:\\Users\\15007\\Documents\\WeChat Files\\VinceLim68\\FileStorage\\File\\2021-03\\厦门2月.xlsx"
# datas = ToolsBox.read_excel(input_file,"Sheet")
# # for data in datas:
# #     ToolsBox.printDic(data)
# # print(datas)
# import pymysql
# conn = pymysql.connect(host ='localhost', user ="root", passwd ="root", db ="yunping", charset ="utf8", port = 3306)  # 链接数据库
# cur = conn.cursor()
# COLstr = ''  # 列的字段
# ROWstr = ''  # 行字段
# dic = datas[0]
# ColumnStyle = ' VARCHAR(20)'
# for key in dic.keys():
#     COLstr = COLstr + ' ' + key + ColumnStyle + ','
#     ROWstr = ROWstr + dic[key] + ','
# insterstr = "INSERT INTO %s VALUES "+ ROWstr[:-1]
# print(insterstr)

def dic2sql(dic, sql):
    sf = ''

    for key in dic:
        tup = (key, dic[key])
        sf += (str(tup) + ',')
    sf = sf.rstrip(',')

    sql2 = sql % sf
    return sql2


dic = {'apple': 216, 'jar': 138}
sql = "insert into users (login,userid) VALUES %s;"

ret = dic2sql(dic, sql)
print(ret)

# def InsertData(TableName, dic):
#     try:
#

#
#         # 判断表是否存在，存在执行try，不存在执行except新建表，再insert
#     try:
#         cur.execute("SELECT * FROM %s" % (TableName))
#         cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))
#
#     except MySQLdb.Error, e:
#         cur.execute("CREATE TABLE %s (%s)" % (TableName, COLstr[:-1]))
#         cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     except MySQLdb.Error, e:
#     print
#     "Mysql Error %d: %s" % (e.args[0], e.args[1])
#
#
# if __name__ == '__main__':
#     dic = {"a": "b", "c": "d"}
#     InsertData('testtable', dic)