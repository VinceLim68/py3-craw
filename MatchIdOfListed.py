import pymysql
import ToolsBox
import MyVote

#挂牌数据匹配出开发库里的小区id值
class MatchIdOfListed(object):

    def __init__(self):
        try:
            self.db = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='yunping',
                           charset='utf8')
        except:
            print( "连接失败！")
        if self.db:
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            self.comm_arr = self.get_comm_arr_fromMysql()

    # 返回开发库里的小区-id名
    # 得到{小区名：id值，小区名：id值，......}
    def get_comm_arr_fromMysql(self):
        sql = "SELECT id,com_name,alias_com_name FROM `t_base_community` WHERE city_name='厦门市'"
        arr = self.get_list_fromMysql(sql)
        # print(len(arr))
        comm_arr = {}
        for item in arr:
            if item['alias_com_name']:
                comms = item['alias_com_name'].split(';')
                for comm in comms:
                    comm = ToolsBox.clearStr(comm)
                    if comm not in comm_arr.keys():comm_arr[comm] = item['id']
            if item['com_name']:
                comm = ToolsBox.clearStr(item['com_name'])
                if comm not in comm_arr.keys():comm_arr[comm] = item['id']
            # 返回key-value值的字典
            # {'城南阳翟教师楼': '04b90367549011ebb98a98039b073fcc', '国联大厦': '04bc8a7f549011ebb98a98039b073fcc'...}
        return comm_arr


    # 得到[{},{},{}]
    def get_list_fromMysql(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 把挂牌数据挂上开发库里的id值
    @ToolsBox.exeTime
    def match_list2comm(self):
        # 取挂牌记录
        ListRecords = ML.get_list_fromMysql("SELECT distinct community_name FROM `ods_hse_detail`")
        for item in ListRecords:
            item['clear_name'] = ToolsBox.clearStr(item['community_name'])

        result = []         # 以开发库的小区名为主，匹配出挂牌数据的列表
        for key,value in self.comm_arr.items():
            name_dic = dict()
            name_dic['comm_name'] = key
            name_dic['comm_id'] = value
            name_dic['vol'] = 0
            name_dic['match_list_comm_name'] = ''
            name_dic['match_all'] = ''      #存放所有匹配度>0.8的小区名
            for item in ListRecords:
                vol = MyVote.cmntVol(key, item['clear_name'])
                if vol > name_dic['vol']:
                    name_dic['vol'] = vol
                    name_dic['match_list_comm_name'] = item['community_name']
                if vol >= 0.8:
                    name_dic['match_all'] = name_dic['match_all'] + item['community_name'] + '(' +'%f'%vol + ');'
            result.append(name_dic)

        for item in ListRecords:
            item['matchid'] = '0'
            item['match_vol'] = 0
            for key, value in self.comm_arr.items():
                vol = MyVote.cmntVol(key,item['clear_name'])
                if vol > item['match_vol']:
                    item['match_vol'] = vol
                    item['matchid'] = value
                    item['match_comm_name'] = key
        ToolsBox.saveExcel('match.xlsx',result,"Sheet1")
        ToolsBox.saveExcel('match.xlsx',ListRecords,"Sheet2")

        # print(ListRecords)


if __name__ == "__main__":
    ML = MatchIdOfListed()
    # comm_arr = ListMatch.get_list_fromMysql("SELECT id,com_name,alias_com_name FROM `t_base_community` WHERE city_name='厦门市'")
    # print(len(ML.comm_arr))
    ML.match_list2comm()
