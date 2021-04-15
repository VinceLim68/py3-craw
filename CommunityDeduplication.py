#小区名称去重模块
import ToolsBox,math,copy
# from openpyxl import Workbook
from openpyxl import load_workbook
from fuzzywuzzy import fuzz

# 专门完成小区去重任务的类
class CommunityDeduplication(object):
    def __init__(self,file_name,col_name,sheet_name="Sheet1"):
        self.IDFDic = {}    #存储全部小区用字的IDF值的字典
        self.file_name = file_name      #输入待匹配的文件名
        self.col_name = col_name        #指明待匹配的字段名，可能是小区名，也可能是地址
        self.sheet_name = sheet_name    #指明所在的表名
        self.input_sheet =[]            #读当前表的全部内容
        self.fuzzPercentage = 0.45      #使用fuzz计算相似度的占比
        self.valve = 0.75               #相似度的阀值

    #根据excel表，得到小区名称中各个字的IDF值，输出dic
    @ToolsBox.exeTime
    def generate_IDF_dic(self, col_name = None):
        if not self.input_sheet:self.input_sheet = ToolsBox.read_excel(self.file_name,self.sheet_name)
        if col_name is None: col_name = self.col_name
        total_row =len(self.input_sheet)
        count_dict = {}
        # 统计数量
        for item in self.input_sheet:
            # item[col_name] = ToolsBox.clearStr(item[col_name])
            # for char in item[col_name]:
            new_item = copy.deepcopy(item)
            new_item[col_name] = ToolsBox.clearStr(new_item[col_name])
            for char in new_item[col_name]:
                count_dict[char] = count_dict[char] + 1 if char in count_dict else 1

        # 求取IDF值
        for k,v in count_dict.items():
            count_dict[k] = math.log(total_row/v)

        # 排序
        count_dict = dict(sorted(count_dict.items(), key = lambda x: x[1], reverse=True))
        # print(count_dict)
        # print(type(count_dict))

        return count_dict

    # 把计算完成的IDF值写入文件
    def IDF_dic_output_excel(self,out_file,sheet_name = "Sheet1"):
        if not self.IDFDic:self.IDFDic = self.generate_IDF_dic()
        # print("IDFDic's type is :%s"%(type(self.IDFDic)))
        ToolsBox.dic2Excel(out_file,self.IDFDic)


    # 从excel文件中生成IDF字典，excel每一行的格式是"字，IDF"
    def generate_IDF_dic_from_file(self,file_name,sheet_name="Sheet1"):
        wb = load_workbook(file_name)
        ws = wb[sheet_name]
        IDF={}
        for row in ws.rows:
            IDF[row[0].value] = row[1].value
        return IDF


    # 顺位匹配，返回两个字符串的交集
    def get_intersection_of_two_words(self,str1, str2):
        try:
            intersection = []
            for char in str1:
                match_location = int(str2.find(char))
                if match_location >= 0:
                    intersection.append(char)
                    str2 = str2[match_location + 1:]
            # if intersection:intersection_IDF = self.get_IDF(intersection)
        except Exception as e:
            print( "countChar(x, y): 错误，错误信息：" + str(e))

        return intersection

    # 输入一个字符组成的[],返回他们的IDF值的｛｝
    def get_word_IDF_dic(self,list):
        if not bool(self.IDFDic):
            self.IDFDic = self.generate_IDF_dic()
        string_IDF_dic ={}
        for char in list:
            string_IDF_dic[char] = self.IDFDic[char]
        # ToolsBox.printDic(word_IDF_dic)
        return string_IDF_dic

    #得到字符串的IDF值
    def get_word_IDFSum(self,IDF_dic):
        # print(sum(IDF_dic.values()))
        return sum(IDF_dic.values())

    # 利用自定义的算法，计算两个词的相似度
    def get_similar(self,str1,str2):
        intersection = self.get_intersection_of_two_words(str1,str2)
        intersection_dic = self.get_word_IDF_dic(intersection)
        # ToolsBox.printDic(intersection_dic)
        # min_str = str1 if len(str1)<=len(str2) else str2
        str1_dic = self.get_word_IDF_dic(str1)
        str2_dic = self.get_word_IDF_dic(str2)
        str_IDFsum = (self.get_word_IDFSum(str1_dic) + self.get_word_IDFSum(str2_dic))/2
        # ToolsBox.printDic(min_str_dic)
        return self.get_word_IDFSum(intersection_dic)/str_IDFsum

    # 获取两个字符串的综合相似度（考虑fuzzy)
    def get_Comprehensive_similar(self,in_str1,in_str2):
        str1 = ToolsBox.clearStr(in_str1).upper()
        str2 = ToolsBox.clearStr(in_str2).upper()
        # str1 = (in_str1).upper()
        # str2 = (in_str2).upper()
        fuzzSimilar = fuzz.ratio(str1, str2) / 100
        # print("fuzz: %f" %(fuzzSimilar))
        selfSimilar = self.get_similar(str1,str2)
        # print("mysimilar:%f"%(selfSimilar))
        return fuzzSimilar * self.fuzzPercentage + selfSimilar * ( 1 - self.fuzzPercentage )

    # 比较两个地址的相似度
    def get_add_com_similar(self,add1:str,add2:str = ""):
        # 把地址拆成路和号分别比较
        add1list = add1.split(r"/d+",1)
        print(add1list)
        # 比较地址
        # 比较门牌号
        # pass

    # 去重模块
    @ToolsBox.exeTime
    def deduplicate(self):
        if not self.input_sheet: self.input_sheet = ToolsBox.read_excel(self.file_name, self.sheet_name)
        # ToolsBox.saveExcel("C:\\Users\\15007\\Desktop\\回写.xlsx", self.input_sheet,"运行前")
        reduce_list = []        #存放去重后的记录的list
        count = 0
        # for record in self.input_sheet:
        for i in range(len(self.input_sheet)):
        # for i in range(1000):
            record = copy.deepcopy(self.input_sheet[i])
            count += 1
            reduce_list_len = len(reduce_list)
            print("第%d个小区：%s(已更新%d个小区)"%(count,record[self.col_name],reduce_list_len))
            # temp_similar_communitys = []        # 一个临时存放相似小区的list
            most_similar_community = {}         # 存放最相似的小区记录
            for item in reduce_list:            # 遍历去重后的小区记录集
                names = item['alias'].split(";")
                for name in names:
                    similar = self.get_Comprehensive_similar(record[self.col_name],name)
                    if similar >= self.valve:
                    # temp_similar_communitys.append(record)
                        if most_similar_community:
                            if most_similar_community['similar'] < similar:
                                # print(">>>>>>>>>>>>>%s与%s原有相似度为%f,现在与%s相似度为%f"%(record[self.col_name],most_similar_community[self.col_name],most_similar_community['similar'],item[self.col_name],similar))
                                print(">>>>>>>>>>>>>%s与%s原有相似度为%f,现在与%s相似度为%f"%(record[self.col_name],most_similar_community[self.col_name],most_similar_community['similar'],name,similar))
                                most_similar_community = item
                                most_similar_community['similar'] = similar
                                # most_similar_community['alias'] = name + ";" + record[self.col_name]
                                print(">>>>>>>>>>>>>>>>>>>>>>>>%s现在最相似小区为%s,相似度为%f"%(record[self.col_name],most_similar_community[self.col_name],most_similar_community['similar']))
                            elif most_similar_community['similar'] == similar:
                                if len(name) > len(most_similar_community[self.col_name]):
                                    print("===========%s与%s原有相似度为%f,现在与%s相似度为%f"%(record[self.col_name],most_similar_community[self.col_name],most_similar_community['similar'],name,similar))
                                    most_similar_community = item
                                    most_similar_community['similar'] = similar
                                    # most_similar_community['alias'] = name + ";" + record[self.col_name]
                                    print("==========================%s现在最相似小区为%s,相似度为%f"%(record[self.col_name],most_similar_community[self.col_name],most_similar_community['similar']))
                                elif len(name) == len(most_similar_community[self.col_name]):
                                    print("???????????????%s与%s原有相似度为%f,现在与%s相似度为%f"%(record[self.col_name],most_similar_community[self.col_name],most_similar_community['similar'],name,similar))
                                    # most_similar_community['alias'] += ";" + record[self.col_name]
                                    ToolsBox.printDic(most_similar_community)
                        else:
                            most_similar_community = item
                            most_similar_community['similar'] = similar
                            # most_similar_community['alias'] = name + ";" + record[self.col_name]
                            print("@@@@@@@@@@@@@@@@@@@%s与%s相似度为%f" % (record[self.col_name], most_similar_community[self.col_name], most_similar_community['similar']))

            if most_similar_community:      #如果小区在“去重集”中找到相似小区，更新一下去重集
                for index in range(reduce_list_len):
                    if reduce_list[index][self.col_name] == most_similar_community[self.col_name]:
                        reduce_list[index]['alias'] = reduce_list[index]['alias'] + ";" + record[self.col_name]
                        break
            else:       # 如果没有发现去重后的小区记录集有与当前记录匹配的，说明是一个新小区，加入“去重集”中
                record['alias'] = record[self.col_name]
                reduce_list.append(record)
        # print(type(reduce_list))
        ToolsBox.saveExcel("C:\\Users\\15007\\Desktop\\去重结果.xlsx",reduce_list)
        # ToolsBox.saveExcel("C:\\Users\\15007\\Desktop\\回写1.xlsx",self.input_sheet,"运行后")





# (generate_IDF_file("重庆.xlsx","小区名称","sheet1"))
# print(get_intersection_of_two_words("奥园城市天地(A区)","奥园城市天地"))
# generate_IDF_dic_from_file("C:\\Users\\15007\\Desktop\\词频结果.xlsx","词频表")
# get_IDF("奥园城市天地(A区)")
# ToolsBox.printDic(IDFDic)
if __name__=="__main__":
    cd = CommunityDeduplication("重庆.xlsx","小区名称","sheet1")
    # cd = CommunityDeduplication("C:\\Users\\15007\\Desktop\\回写.xlsx","小区名称","Sheet1")
    # cd.IDF_dic_output_excel("C:\\Users\\15007\\Desktop\\词频结果.xlsx","词频表")
    # print(cd.get_intersection_of_two_words("奥园城市天地(A区)","奥园城市天地"))
    # ToolsBox.printDic(cd.get_IDF("奥园城市天地(A区)"))
    # print(cd.get_Comprehensive_similar('斌鑫新华苑二期','斌鑫新华苑一期'))
    # 地址匹配：字符包含就算匹配成功，比例对半
    # 把地址拆分成“路”“号”“路+号”三部分分别匹配，各占33%，但是没有号的，这33%的部分直接取0
    # 小区名匹配：字符需要完全匹配才算匹配成功，fuzzy比例0.45
    # 价格匹配
    # 地址匹配*0.35 + 小区名称匹配 * 0.65
    cd.deduplicate()
    # str = "光华大厦;光宇大厦;国华大厦;华川大厦;华雅大厦;华宇大厦;华宇大厦小区;华宇龙泉大厦"
    # comms = str.split(";")
    # for i in comms:
    #     for j in comms:
    #         if i != j :
    #             simi = cd.get_Comprehensive_similar(i,j)
    #             if simi >= 0.72:print("%s和%s相似度为%.8f"%(i,j,simi))
