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
new_url = 'http://xm.anjuke.com/sale/p1-rd1/?kw=%E5%AE%89%E5%85%A8%E5%B1%80%E5%AE%BF%E8%88%8D&from_url=kw_final#filtersort'
print(new_url)
match_comm = re.findall(r'kw=(.*)&from_url', new_url)
# ToolsBox.printDic(match_comm)
print(unquote(match_comm[0],'utf-8')=='安全局宿舍')