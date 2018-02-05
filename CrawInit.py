import pymysql
import datetime
import traceback

class CrawInit(object):
    # 在抓取数据之前，先把指定时间之间的记录移到总库中去。
    def __init__(self):
        try:
            self.conn=pymysql.connect(host = "office.xmcdhpg.cn",user = "root",passwd = "root",db = "property_info",charset = "utf8",port = 6153)
        except:
            print( "Connect failed")
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.rows = []

    def get_datas(self):
        #从数据库里读取指定时期的记录

        sql = """
            SELECT * FROM for_sale_property where 
            first_acquisition_time >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH )
        """
        self.cur.execute(sql)
        self.rows = self.cur.fetchall()
        print(len(self.rows))

    def insert_datas(self):
        # 把记录插入总库中
        dupli = 0       #计数：插入数据库时的重复记录值
        success = 0     #计数：插入数据库的成功记录数量
        sql = """
                    INSERT allsales (title,area,spatial_arrangement,price,floor_index,
                    total_floor,builded_year,advantage,total_price,details_url,community_name,
                    first_acquisition_time,from_,community_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        for data in self.rows:
            try:
                self.cur.execute(sql,(data['title'],data['area'],data['spatial_arrangement'],data['price'],
                    data['floor_index'],data['total_floor'],data['builded_year'],data['advantage'],data['total_price'],
                    data['details_url'],data['community_name'],data['first_acquisition_time'],data['from_'],data['community_id']))
                success = success + 1
                self.conn.commit()
                print(success)
            except pymysql.err.IntegrityError as e:
                if e.args[0] == 1062 :
                    dupli = dupli + 1
                else:
                    with open('logtest.txt','a+') as fout:
                        fout.write(str(datetime.datetime.now()) + 'record by CrawInit \n')
                        traceback.print_exc(file=fout)
                    print(traceback.format_exc())
                    code, message = e.args
                    print(code,message)
            except pymysql.err.InternalError as e:
                with open('logtest.txt','a+') as fout:
                    fout.write(str(datetime.datetime.now()) + 'record by CrawInit \n')
                    traceback.print_exc(file=fout)
                    print(traceback.format_exc())
                code, message = e.args
                print(code,message)

        print("本次共{0}个数据，存入{1},重复{2}".format(len(self.rows),success,dupli))


    def del_datas(self):
        # 删除记录
        pass

    def close_db(self):
        self.cur.close()
        self.conn.close()
        return

if __name__=="__main__":
    start = CrawInit()
    start.get_datas()
    start.insert_datas()
    start.close_db()