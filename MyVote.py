# -*- coding: utf-8 -*-

""" 开始 : 字符串处理部分 """

# 导入Python资源库
import re

# 字符串处理函数 函数清洗时间 0.002s ~ 0.003s
def strRpl(mystr):
    """ 清除不必要的字符,成功返回清洗后的数据，失败返回 '' """
    # 返回值
    my_result = ''
    # 清洗过程
    try:
        # 匹配不是中文、大小写、数字的其他字符
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^-^—^|^、^,]") 
        # 将string1中匹配到的字符替换成空字符
        my_result = cop.sub('', mystr)
        # 转换成大写字母
        my_result = str(my_result).upper().strip()
    except Exception as e:
        my_result = ''
    # 过滤掉可能出现的NULL值
    my_result = str(my_result).replace('None','').replace('NONE','').strip()
    if my_result is None:
        my_result = ''
    # 非NULL值要替换掉|和；
    if my_result != '':
        try:
            my_result = my_result.replace('|',';').replace('；',';')
        except Exception as e:
            my_result = ''

    # 返回最终值
    return my_result

# 数字处理函数 耗时 0s ~ 0.001s
def numRpl(mynum):
    """ 把字符串的数字转成浮点数，成功返回float,失败返回-1 """
    # 返回值
    my_result = -1
    # 转换过程
    try:
        # 把字符串数字转成浮点数
        my_result = float(mynum)
    except Exception as e:
        my_result = -1
    #返回值
    return my_result

# 地址拆分出道路 耗时 0.001s
def addrbefore(myaddr):
    """ 从地址中拆分出道路名，把数字+号或数字加弄前面的道路取出，返回道路名，失败返回 '' """
    # 返回值
    my_result = ''
    try:
        # 正则
        pattern = re.compile(r'\d?[^\u4e00-\u9fa5]?\d+')
        n = re.search(pattern, myaddr, flags=0)
        # 将string1中匹配到的字符替换成空字符
        if n is not None:
            loc = n.span()[0]
            my_result = str(myaddr)[:loc]
        else:
            my_result = myaddr
    except Exception as e:
        my_result = ''
    # 返回返回值
    return my_result

# 地址拆分出号 耗时 0.001s ~ 0.003s
def addrnumber(addr):
    """ 从地址中把号前的数字或者弄前的数字取出，成功返回数字，失败返回 '' """
    # 返回值
    my_result = ''
    # 正则过程
    try:
        pattern = re.compile(r'\d+[号弄苑]+')
        n = re.search(pattern, addr, flags=0)
        if n is None:
            my_result = ''
        else:
            num_str = n.group(0)
            pattern2 = re.compile(r'\d+')
            n2 = re.search(pattern2, num_str, flags=0)
            if n2 is None:
                my_result = ''
            else:
                my_result = int(n2.group(0))
    except Exception as e:
        my_result = ''
    # 返回函数值
    return my_result

""" 结束 : 字符串处理部分 """

# ———————————————————————————————————————————————
# 啊哈哈哈哈哈~~~ 我是可爱的分割线~~~~~ 啦啦啦啦~~~~
# ———————————————————————————————————————————————

""" 开始 ： 相似度计算部分 """

import math
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# 顺位匹配，计算最大共有字符数量 耗时 0s
def countChar(str1, str2):
    """ 顺位匹配，计算最大共有字符数量 返回最大共有字符数量 """
    # 共有字符数量
    matchchar_num = 0
    # 计算过程
    try:
        # 被匹配字符的长度
        str1_len = len(str1)
        # 共有数量初始化
        matchchar_num = 0
        # 遍历被匹配字符串
        for i in range(0,str1_len):
            # 被匹配的字符
            for_match_char = str1[i]
            # 查找被匹配字符在 匹配字符串的位置
            match_location = int(str2.find(for_match_char))
            # 如果字符在匹配字符串中存在
            if match_location >= 0:
                # 共有字符数量 + 1
                matchchar_num += 1
                # 切割匹配的字符串
                str2 = str2[match_location+1:]
    except Exception as e:
        matchchar_num = 0
    # 返回函数值
    return  matchchar_num

# 小区名相似度计算 ，建议小区名相似度大于0.7的时候考虑地址不同的合并问题 耗时 0s ~ 0.002S
def cmntVol(s1, s2):
    """ 计算两个小区名的相似度:
        1.判断两个字符串是否相等，相等相似度为1 ，
        2.判断两个字符串是否包含，包含则降低一点相似度，否进入下一步
        3.顺位匹配*0.75 + fuzzywuzzy * 0.25 或 顺位匹配*0.65 + fuzzywuzzy * 0.35
        4.小区名过短的情况下需要降相似度
        5.如果是最后一个字不一样则增加相似度
        6.返回相似度 
    """
    # 小区名相似度
    Vol = 0
    # 如果两个小区名任一为空，则相似度为 -1
    if s1 == '' or s2 == '':
        return -1
    # 两个小区名一模一样且都不为空，相似度为 1
    if s1 == s2:
        return 1
    else:
        # 两个小区名不为空且不相同
        # 如果 s1 包含 s2, 计算字符长度差，按照每个字符 0.01 减少
        if s1.find(s2) != -1 or s2.find(s1) != -1:
            # 计算各个字符串长度
            ls1 = len(s1)
            ls2 = len(s2)
            lnc = ls2 - ls1
            if lnc < 0:
                lnc = lnc * -1
            Vol = 1 - (lnc * 0.01)
        
        else:
            # 如果 s1 和 s2 不包含，
            # 计算各个字符串长度
            ls1 = len(s1)
            ls2 = len(s2)
            # 寻找最小的字符长度
            minlen = min(ls1, ls2)
            # 寻找最大的字符长度
            maxlen = max(ls1, ls2)
            # 寻找两个字符串的最大共有字符串
            maxnum = countChar(s1, s2)
            vol_mine = 0
            vol_min = -1
            vol_max = -1
            # 计算最小字符长度占比
            if minlen > 0:
                vol_min = maxnum / minlen
            # 计算最长字符长度占比
            if maxlen > 0:
                vol_max = maxnum / maxlen
            # 自己的相似度
            if vol_min == -1 and vol_max == -1:
                vol_mine = 0
            else:
                if vol_max == -1:
                    vol_mine = vol_min
                if vol_min == -1:
                    vol_mine = vol_max
                if vol_max != -1 and vol_min != -1:
                    vol_mine = vol_min * 0.9 + vol_max * 0.1
            
            # 计算Myfuzzy占比
            vol_fuzzy = -1
            try:
                vol_fuzzy = fuzz.ratio(s1, s2) / 100
            except Exception as e:
                vol_fuzzy = -1
            # 合并fuzzy相似度和自己相似度
            if vol_fuzzy != -1:
                if vol_mine >= 0.6:
                    Vol = 0.75 * vol_mine + 0.25 * vol_fuzzy
                else:
                    Vol = 0.65 * vol_mine + 0.35 * vol_fuzzy
            if Vol > 1:
                Vol = 1
            #print("Vol:",Vol, "Vol1:", vol_mine, "Vol2:", vol_fuzzy)
            # 如果小区名的长度较短 , 多减去部分相似度
            if (ls1 <= 5 and ls1 >=3) or (ls2 <= 5 and ls2 >= 3):
                Vol = Vol - (((1 / minlen) * 0.2) * 0.4 + ((1 / maxlen) *0.2) * 0.6)
                if Vol < 0:
                    Vol = 0  
            #print("Vol:",Vol, "Vol1:", vol_mine, "Vol2:", vol_fuzzy)
            # 如果是最后一个字不一样则增加权重
            if (minlen - maxnum) == 1:
                s1t = s1[:-1]
                s2t = s2[:-1]
                if s1t == s2t:
                    Vol = Vol + (1 - Vol) * 0.7
                else:
                    if s1t.find(s2t) or s2t.find(s1t):
                        Vol = Vol + (1 - Vol) * 0.23
    Vol = round(Vol, 4)

    # 返回值
    return Vol

# 地址号相差处理函数，返回应该减去的相似度值,耗时 0s
def delLocNum(num1, num2):
    """ 传入两个地址的号，
        任一空值扣 0.09
        相差 50 号以内扣 0.012，
        相差 50 - 150 号扣 0.045
        相差 150 号以上扣 0.085
        返回应该减去的相似度值，浮点数型 """
    
    # 最终要减去的相似度
    Vol = 0
    # 号任意一个为空
    if num1 == '' or num2 == '':
        Vol = 0.035
    else:
        # 号不为空
        # 获取地址号的差值
        num_nc = num2 - num1
        if num_nc < 0:
            num_nc = num_nc * -1
        # 根据情况增加要扣除的相似度
        if num_nc == 0:
            Vol = 0
        elif num_nc < 50:
            Vol = 0.012
        elif num_nc >=50 and num_nc < 150:
            Vol = 0.053
        else:
            Vol = 0.121
    # 返回最终要减去的相似度
    return Vol

# 地址相似度计算 ， 建议相似度 0.8 以上，耗时 ：0.001 ~ 0.002s
def addrVol(s1, s2):
    """ 计算两个地址的相似度
        1.判断两个字符串是否相等或者包含，相等相似度为1 否则进入下一步，
        2.顺位匹配*0.5 + fuzzywuzzy * 0.5
        3.返回相似度 
    """
    # 最终相似度
    Vol = 0
    # 判断地址是否任意一个为空，返回-1
    if s1 == '' or s2 == '':
        return -1
    # 判断地址是否完全一样
    if s1 == s2:
        return 1
    # 判断地址是否相互包含，是的话根据情况降低一点相似度
    else:
        # 获取地址的道路名
        loc1 = addrbefore(s1)
        loc2 = addrbefore(s2)
        # 地址道路名的长度
        l1 = len(loc1)
        l2 = len(loc2)
        # 最大长度
        max_len = max(l1, l2)
        # 最小长度
        min_len = min(l1, l2)
        # 获取地址的号
        num1 = addrnumber(s1)
        num2 = addrnumber(s2)
        # 要减去的相似度值
        vol_del = delLocNum(num1, num2)
        # 如果地址道路名任一为空
        if loc1 == '' or loc2 == '':
            return -1
        else:
            # 道路名都不为空
            if loc1 == loc2:
                # 道路名相同
                Vol = 1 - vol_del
            else:
                # 道路名任一包含
                if loc1.find(loc2) != -1 or loc2.find(loc1) != -1:
                    # 计算长度差值,扣去相差字符数乘以0.01
                    len_nc = l2 - l1
                    if len_nc < 0:
                        len_nc = len_nc * -1
                    Vol = 1 - (len_nc * 0.01)
                    Vol = Vol - vol_del
                    if Vol < 0:
                        Vol = 0
                else:
                    # 如果道路名不一样
                    # 计算最大公有字符
                    maxnum = countChar(loc1, loc2)
                    vol_mine = 0
                    # 最大长度占比
                    vol_max = -1
                    if max_len > 0:
                        vol_max = maxnum / max_len
                    # 最小长度占比
                    vol_min = -1
                    if min_len > 0:
                        vol_min = maxnum / min_len
                    # 计算顺位相似度
                    if vol_min != -1 and vol_max != -1:
                        vol_mine = vol_min * 0.85 + vol_max * 0.15
                    else:
                        if vol_min == -1:
                            vol_mine = vol_max
                        else:
                            vol_mine = vol_min
                    # 计算Fuzzy占比
                    vol_fuzzy = -1
                    try:
                        vol_fuzzy = fuzz.ratio(loc1, loc2) / 100
                    except Exception as e:
                        vol_fuzzy = -1
                    if vol_fuzzy == -1:
                        Vol = vol_mine
                    else:
                        if vol_mine >= 0.6:
                            Vol = vol_mine * 0.75 + vol_fuzzy * 0.25
                        else:
                            Vol = vol_mine * 0.6 + vol_fuzzy * 0.4
                    
                    # 如果地址的长度较短 , 多减去部分相似度
                    if (l1 <= 5 and l1 >=3) or (l2 <= 5 and l2 >= 3):
                        Vol = Vol - ((1 / min_len) * 0.25)* 0.4 + ((1 / max_len) * 0.35)* 0.7
                        if Vol < 0:
                            Vol = 0  
                 
                    Vol = Vol - vol_del
                    if Vol < 0:
                        Vol = 0
                    
                    # 如果是最后一个字不一样则增加权重
                    if (min_len - maxnum) == 1:
                        s1t = loc1[:-1]
                        s2t = loc2[:-1]
                        if s1t == s2t:
                            Vol = Vol + (1 - Vol) * 0.85     
    Vol = round(Vol, 4)
    # 返回相似度
    return Vol  

# 计算拼音的相似度 好耗时 0.001s
def pinyinVol(p1, p2):
    """ 把两个拼音字符串进行相似度匹配，返回相似度值 """
    # 相似度
    Vol = 0
    # 如果任一为空
    if p1 == '' or p2 == '':
        return -1
    # 如果两个相同
    if p1 == p2:
        Vol = 1
    else:
        # 如果两个不相同
        # 字符长度
        l1 = len(p1)
        l2 = len(p2)
        # 最大字符长度
        max_len = max(l1, l2)
        # 最小字符长度
        min_len = min(l1, l2)
        # 计算最大公有字符数量
        maxnum = countChar(p1, p2)
        # 计算最小字符长度占比
        vol_min1 = -1
        if min_len > 0:
            vol_min1 = maxnum / min_len
        # 计算最大字符长度占比
        vol_max1 = -1
        if max_len > 0:
            vol_max1 = maxnum / max_len
        # 计算顺位相似度
        vol_mine = 0
        if vol_min1 != -1 and vol_max1 != -1:
            vol_mine = vol_min1 * 0.85 + vol_max1 * 0.15
        else:
            if vol_max1 == -1:
                vol_mine = vol_min1
            else:
                vol_mine = vol_max1
        
        # 计算Fuzzy占比
        vol_fuzzy = -1
        try:
            vol_fuzzy = fuzz.ratio(p1, p2) / 100
        except Exception as e:
            vol_fuzzy = -1
        if vol_fuzzy == -1:
            Vol = vol_mine
        else:
            if vol_mine >= 0.6:
                Vol = vol_mine * 0.85 + vol_fuzzy * 0.15
            else:
                Vol = vol_mine * 0.7 + vol_fuzzy * 0.3
            
    # 返回值
    return Vol

# 均价相差范围
pr_vote = 0.15

# 均价差值计算函数, 返回需要处理的相似度，相加即可，耗时 0s
def priceVol(p1, p2):
    """ 计算两个均价是否在一个范围内，是就增加一点相似度，否则减少一些相似度，如果有一个为空，则不增加也不减少 """
    # 要相加的相似度
    Vol = 0
    # 如果任意一个为空
    if p1 == -1 or p1 == 0 or p2 == 0 or p2 == -1:
        # 其中一个为空
        return 0
    else:
        # 如果两个都不为空
        if p1 != -1 and p1 != 0:
            if p2 != -1 and p2 != 0:
                pr_nc = p2 - p1
                if pr_nc < 0:
                    pr_nc = pr_nc * -1
                min_price = min(p1, p2)
                pr_temp = pr_nc / min_price
                if pr_temp <= pr_vote:
                    Vol = 0.1
                else:
                    Vol = -0.25
    
    # 返回值
    return Vol

#地图比例大小，0.01指1公里
loat_zt = 0.01

# 坐标位置比较，返回要处理的相似度, 耗时 0.001s
def loatVol(a1, a2, b1, b2):
    """ 坐标位置判断，返回需要处理的相似度，相加即可，符合距离，相似度 +1 ，否则 -0.25，没有坐标，增加相似度为0 """
    # 相似度值
    Vol = 0
    if a1 == -1 or a2 == -1 or b1 == -1 or b2 == -1:
        Vol = 0
    else:
        # 计算经度
        x = a1 - b1
        if x < 0:
            x = x * -1
        # 计算维度
        y = a2 - b2
        if y < 0:
            y = y * -1
        
        # 计算距离
        zt = x * x + y * y
        z = math.sqrt(zt)

        # 安居客
        if z <= loat_zt:
            Vol = 1
        else:
            Vol = -0.25
    # 返回相似度
    return Vol
    
# 获取两个数据相似度的函数， 耗时 0.001 ~ 0.002s
def getMyVote(ar, br):
    """ 
    获取两条数据的相似度
    A. 参数格式：["福建省", "厦门市", "思明区", "米兰春天", "金桥路22号", 54876, 120, 150, "milanchuntian", "jinqiaolu22hao"]
    B. 返回值：浮点数。 范围： 0 ~ 1
    """
    # 相似度
    Vol = 0
    #获取数据
    a_prov = ar[0]
    a_city = ar[1]
    a_region = ar[2]
    a_name = ar[3]
    a_loc = ar[4]
    a_price = ar[5]
    a_lot = ar[6]
    a_lat = ar[7]
    a_py_nm = ar[8]
    a_py_loc = ar[9]
    # 获取B数据
    b_prov = br[0]
    b_city = br[1]
    b_region = br[2]
    b_name = br[3]
    b_loc = br[4]
    b_price = br[5]
    b_lot = br[6]
    b_lat = br[7]
    b_py_nm = br[8]
    b_py_loc = br[9]
    # 省市区判断
    is_Matched = True
    # 判断省是否相同
    if a_prov != "" and b_prov != "":
        if a_prov != b_prov:
            is_Matched = False
    # 判断市是否相同
    if a_city != '' and b_city != "":
        if a_city != b_city:
            is_Matched = False
    # 判断区是否相同
    if a_region != "" and b_region != "":
        if a_region != b_region:
            is_Matched = False
    # 省市区完成判断后
    if is_Matched == False:
        return Vol
    else:
        # 小区名相似度
        nm_vol1 = cmntVol(a_name, b_name)
        # 小区名拼音相似度
        nm_vol2 = pinyinVol(a_py_nm, b_py_nm)
        # 地址相似度
        loc_vol1 = addrVol(a_loc, b_loc)
        # 地址拼音相似度
        loc_vol2 = pinyinVol(a_py_loc, b_py_loc)

        # 整合相似度
        if nm_vol1 == -1:
            # 小区名有空值
            if loc_vol1 == -1:
                # 地址为空，返回0
                return 0
            else:
                # 地址不为空
                # 整合地址相似度
                # 地址拼音相似度是 -1
                if loc_vol2 == -1:
                    if loc_vol1 != -1:
                        Vol = loc_vol1
                else:
                    Vol = loc_vol1 * 0.85 + loc_vol2 * 0.15
        else:
            # 小区名不为空
            # 如果小区名拼音的相似度是 -1
            nm_vol_all = 0
            if nm_vol2 == -1:
                if nm_vol1 != -1:
                    nm_vol_all = nm_vol1
            else:
                nm_vol_all = nm_vol1 * 0.9 + nm_vol2 * 0.1
            # 整合地址的相似度
            loc_vol_all = 0
            # 如果地址相似度为-1
            if loc_vol1 == -1:
                loc_vol_all = -1
            else:
                if loc_vol2 != -1:
                    loc_vol_all = loc_vol1 * 0.85 + loc_vol2 * 0.15
                else:
                    loc_vol_all = loc_vol1
            # 小区名相似度极高的情况下减少地址的影响程度
            if nm_vol_all >= 0.72:
                if loc_vol_all != -1:
                    Vol = nm_vol_all * 0.86 + loc_vol_all * 0.14
                else:
                    Vol = nm_vol_all
            else:
                if loc_vol_all != -1:
                    Vol = nm_vol_all * 0.5 + loc_vol_all * 0.5
                else:
                    Vol = nm_vol_all
            #print('test:','nm_vol',nm_vol_all,'loc_vol',loc_vol_all,'Vol',Vol)
    # 判断均价
    pr_vol = priceVol(a_price, b_price)
    Vol = Vol + pr_vol
    if Vol > 1:
        Vol = 1
    # 判断坐标
    loat_vol = loatVol(a_lot, a_lat, b_lot, b_lat)
    Vol = Vol + loat_vol
    if Vol > 1:
        Vol = 1
    # 返回相似度
    #print(Vol)
    return Vol

""" 结束 ： 相似度计算部分 """

# ———————————————————————————————————————————————
# 啊哈哈哈哈哈~~~ 我是可爱的分割线~~~~~ 啦啦啦啦~~~~
# ———————————————————————————————————————————————

""" 主函数 """

if __name__ == '__main__':
    pass
   