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
# print(len(match_comm)==1)
string = '高楼层(共6层) 1室1厅 | 31.25平米 | 南'
# a =string.split('|').split(' ')
a = re.split(r'\s*[|,\s]\s*',string)
print(a)
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