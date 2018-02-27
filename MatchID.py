import pymysql
import ToolsBox

class MatchID(object):
    """
    将挂牌信息中的小区名称匹配成相应的小区id的对象
    """
    __instance = None

    def __init__(self):
        try:
            self.db = pymysql.connect(host ='office.xmcdhpg.cn', user ="root", passwd ="root", db ="property_info", charset ="utf8", port = 6153)
        except:
            print( "连接失败！")
        if self.db:
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            self.comm_arr = self.get_comm_arr_fromMysql(0)
            self.road_arr = self.get_comm_arr_fromMysql(1)

    # 单例。
    def __new__(cls,*args,**kwd):
        if MatchID.__instance is None:
            MatchID.__instance = object.__new__(cls,*args,**kwd)
        return MatchID.__instance

    def get_comm_arr_fromMysql(self,pri):
        # 从comm表，生成comm数组
        # 按关键字进行了拆分，一个id会有多个关键字
        # 返回：每个comm_arr按[id,小区关键字]  
        where = "where pri_level=" + str(pri)
        sql = "SELECT comm_name,comm_id,keywords,pri_level FROM comm " + where
        self.cursor.execute(sql)
        datas = self.cursor.fetchall()
        comm_arr = []
        for data in datas:
            comms = data['keywords'].split(',')     #data[2] = keywords,把keywords用“,”进行拆分
            for comm in comms:
                kv = []
                kv.append(data['comm_id'])
                kv.append(comm)
                comm_arr.append(kv)     
        return comm_arr

    def get_id_from_arr(self,data,comm_arr):
        # 传入一条挂牌记录(list)，匹配出与小区id相关的数组
        # 都是在小区名里寻找是否能匹配到关键字

        commName = data['community_name'].replace("·","").replace(".","").upper()

        getid = []              # getid:[开始位置，关键字，comm_id]
        
        # 轮询小区id与其关键字的对应数组
        for i in comm_arr:                              
            # i[1]=keywords ，关键字后带辅助字的，先将关键字与辅助字拆开
            key_words = i[1].split("/")
            lenth = len(key_words)      #根据lenth判断是否有辅助字
            # 在小区名称中查找关键字，不含辅助字
            start = commName.find(key_words[0].upper())         
            
            # 如果找到
            if start >= 0:
                # 如果有带辅助字，必须同时匹配到辅助字才可以
                if lenth > 1:
                    if data['title']:
                        formatch = commName + data['title'].upper()
                    else:
                        formatch = commName

                    # 在formatch中查找辅助字
                    for j in range(1,lenth):
                        # 只要找到一个，说明符合条件，即可退出循环
                        if formatch.find(key_words[j].upper()) >=0:     
                            #如果是有关键字的，起始位置提前一点，这样会优先于没有关键字的匹配
                            temp = [start-0.5,key_words[0].upper(),i[0]]    #key_words[0] = keyword , key_words[1]以后的是辅助字
                            getid.append(temp)                          #i[0]就是comm_id
                            break
                # 如果没有辅助字
                else:
                    temp = [start,key_words[0].upper(),i[0]]            
                    getid.append(temp)
            else:
                # 如果没有匹配上，就到title里去找一下
                if data['title']:
                    formatch = commName + data['title'].upper()
                else:
                    formatch = commName
                start1 = formatch.find(key_words[0].upper())

                # 如果找到
                if start1 >= 0:
                    # lenth>1,表示有辅助字，必须同时匹配到辅助字才可以
                    if lenth > 1:
                        # 在formatch中查找辅助字
                        for j in range(1, lenth):
                            # 只要找到一个，说明符合条件，即可退出循环
                            if formatch.find(key_words[j].upper()) >= 0:
                                # 如果是有关键字的，起始位置提前一点，这样会优先于没有关键字的匹配
                                temp = [start1 - 0.5, key_words[0].upper(),
                                        i[0]]  # key_words[0] = keyword , key_words[1]以后的是辅助字
                                getid.append(temp)  # i[0]就是comm_id
                                break
                    # 如果没有辅助字
                    else:
                        temp = [start1, key_words[0].upper(), i[0]]
                        getid.append(temp)


                # 返回：[起始位置，关键字，id]
        return getid

    def get_datas(self,n,step,tablename):
        #从数据库里按要求查出挂牌记录集        
        # sql = "SELECT id,title,community_name FROM for_sale_property WHERE community_id < 999 ORDER BY id LIMIT " + str(n) + "," + str(step)
        sql = "SELECT id,title,community_name FROM " + tablename + " WHERE community_id < 999 ORDER BY id LIMIT " + str(n) + "," + str(step)

        self.cursor.execute(sql)
        datas = self.cursor.fetchall()
        return datas

    def update_id(self,dataid,comm_id,table):
        # 把匹配成功的commid写入表中
        sql_update = "UPDATE " + table + " SET community_id = %s WHERE id = %s"
        #print(dataid)
        try:
            result = self.cursor.execute(sql_update,(comm_id,dataid))
            self.db.commit()
        except Exception as e:
            print(e.args[0])
            if e.args[0] == 1062:
                # 如果重复就把它删除
                sql_del = 'DELETE FROM ' + table + ' WHERE id = %s'
                # print(sql_del)
                self.cursor.execute(sql_del,(dataid))
                self.db.commit()
                print('成功删除{0}'.format(dataid))
            result = False
        return result

    def handle_match_mul(self,data,getid):
        """
        处理 getid 中匹配成功不止一个id
        处理的原则是以起始字段在前的为准，
        如果起始字段相同，则以字符串长的为准
        如果起始与字串长度都一样，则人工判断
        """
        flag = False                            #标志位，如果能解析出唯一id,则标志位设成ture
        
        getid.sort(key=lambda x:x[0])           #按照匹配关键字的起始位置排序     
        
        #起始位置最小的getid
        first = getid[0]
        
        # 用第一个匹配成的合成一个字段：起始位置+小区名称+小区id
        # get = str(getid[0][0]) +',' + str(getid[0][1]) +',' + str(getid[0][2]) + "/"      
        # 传进getid,挑选出get
        get = getid[0]
        
        for l in range(1,len(getid)):
            # 如果第二个匹配到的关键字起始位置大于第一个，就以第一个为准，不用再匹配了
            if(getid[l][0] > first[0]):         
                break
            else:                               #如果有并列第一：
                if len(getid[l][1]) > len(first[1]):        #字符串长的优先
                    first = getid[l]
                elif len(getid[l][1]) == len(first[1]):     #字符串长度相同的，标志位设成ture,要人工判断一下
                    # 起始位置相同，关键字长度相同，不知道是哪个小区了
                    get.append(getid[l])
                    # get += str(getid[l][0]) +',' + str(getid[l][1]) +',' + str(getid[l][2]) + "/"
                    flag = True
        # 匹配成功写入一张表，没成功就写入另一张表。
        # 其实不用，成功就写进id,没成功就空着即可
        if flag:
            print('=============匹配多个小区id=================')
            ToolsBox.printDic(data)
            return len(get)
        else:
            return first[2]

    def close_db(self):
        self.cursor.close()
        self.db.close()

    def matchid(self,data):
        # comm_id = ''
        getid = self.get_id_from_arr(data, self.comm_arr)
        try:
            if len(getid) == 1:  # 如果匹配到唯一id
                # self.update_id(data['id'], getid[0][2])
                comm_id = getid[0][2]
            elif len(getid) == 0:  # 如果没匹配到comm，就看看按road是否能匹配
                getroad = self.get_id_from_arr(data, self.road_arr)
                if len(getroad) == 1:  # 匹配到唯一road
                    # self.update_id(data['id'], getroad[0][2])
                    comm_id = getroad[0][2]
                elif len(getroad) == 0:
                    #如果连road也没匹配成功，空在那里
                    # self.insert_err(data)
                    print("---------未匹配成功---------")
                    ToolsBox.printDic(data)
                    comm_id = 0
                elif len(getroad) > 1:  # 如果匹配到不止一个road,进行处理
                    comm_id = self.handle_match_mul(data, getroad)
            elif len(getid) > 1:  # 如果comm匹配到不止一个，进行处理
                comm_id = self.handle_match_mul(data, getid)

        except MySQLdb.Error as e:
            if e.args[0] == 1062:
                print(str(dupli) + "aready have")
                # dupli = dupli + 1

        return comm_id
        # self.close_db()

    def get_and_update(self,tablename):
        n = 0
        step = 150000
        datas = self.get_datas(n, step, tablename)
        input('当前库为{0},共有{1)条记录待处理，按任意键继续....'.format(tablename,len(datas)))
        for data in datas:
            commid = self.matchid(data)
            if commid > 999:
                resu = self.update_id(data['id'], commid,tablename)
                print('result is {0} from {1}'.format(resu,tablename))
                if(resu):
                    self.matchnum += 1
                    print(commid)
                else:
                    print('记录{0}没改成，小区id是{1}'.format(data['id'],commid))

    def matchall(self):
        # 这是一个一次性计算所有未取得id记录的匹配模块

        self.matchnum = 0
        # 先从总库取
        self.get_and_update('allsales')
        print('一共匹配了{0}个记录'.format(self.matchnum))

        # 再从当前库取
        self.get_and_update('for_sale_property')
        print('一共匹配了{0}个记录'.format(self.matchnum))
        self.close_db()
if __name__=="__main__":

    matchid = MatchID()
    matchid.matchall()