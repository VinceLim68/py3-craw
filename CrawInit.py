import pymysql
import datetime
import traceback


class CrawInit(object):
    # 在抓取数据之前，先把指定时间之间的记录移到总库中去。
    def __init__(self):
        try:
            self.conn = pymysql.connect(host="office.xmcdhpg.cn", user="root", passwd="root", db="property_info",
                                        charset="utf8", port=6153)
        except:
            print("Connect failed")
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.rows = []
        self.where = 'first_acquisition_time < DATE_SUB(CURDATE(), INTERVAL 3 month )'
        # self.where = '1=1'

    def gt_max_FAT(self):
        # 获得最大的时间
        sql = "select max(first_acquisition_time) as maxd from allsales"
        self.cur.execute(sql)
        # rows1 =
        self.maxd = self.cur.fetchall()[0]['maxd']
        print(self.maxd)
        # i = 0
        # for date in self.rows:
        #     i += 1
        #     print(i)
        #     if date['first_acquisition_time'] > maxd:
        #         print('true')
        #     else:
        #         print('false')

    def get_datas(self):
        # 从数据库里读取指定时期的记录

        sql = "SELECT * FROM for_sale_property where " + self.where
        # print(sql)
        self.cur.execute(sql)
        self.rows = self.cur.fetchall()
        print(len(self.rows))

    def insert_datas(self):
        # 把记录插入总库中
        dupli = 0  # 计数：插入数据库时的重复记录值
        success = 0  # 计数：插入数据库的成功记录数量
        skip1 = 0  # 计数：忽略的记录（总库中已经有相应的时间的记录）
        sql = """
                    INSERT allsales (title,area,spatial_arrangement,price,floor_index,
                    total_floor,builded_year,advantage,total_price,details_url,community_name,
                    first_acquisition_time,from_,community_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        for data in self.rows:
            if date['first_acquisition_time'] > self.maxd:
                # 如果日期比总库里的新才追加，总库根据日期来判断重复
                try:
                    self.cur.execute(sql, (data['title'], data['area'], data['spatial_arrangement'], data['price'],
                                           data['floor_index'], data['total_floor'], data['builded_year'],
                                           data['advantage'], data['total_price'],
                                           data['details_url'], data['community_name'], data['first_acquisition_time'],
                                           data['from_'], data['community_id']))
                    success = success + 1
                    self.conn.commit()
                    print(success)
                except pymysql.err.IntegrityError as e:
                    if e.args[0] == 1062:
                        dupli = dupli + 1
                    else:
                        with open('logtest.txt', 'a+') as fout:
                            fout.write(str(datetime.datetime.now()) + 'record by CrawInit \n')
                            traceback.print_exc(file=fout)
                        print(traceback.format_exc())
                        code, message = e.args
                        print(code, message)
                except pymysql.err.InternalError as e:
                    with open('logtest.txt', 'a+') as fout:
                        fout.write(str(datetime.datetime.now()) + 'record by CrawInit \n')
                        traceback.print_exc(file=fout)
                        print(traceback.format_exc())
                    code, message = e.args
                    print(code, message)
            else:
                skip1 += 1
        print("本次共{0}个数据，忽略{1},存入{2},重复{3}".format(len(self.rows), skip1, success, dupli))

    def del_datas(self):
        # 删除记录
        sql = 'DELETE FROM for_sale_property WHERE ' + self.where
        sta = self.cur.execute(sql)
        print(sta)
        if sta >= 1:
            print('删除成功')
        else:
            print('删除失败')
        self.conn.commit()

    def close_db(self):
        self.cur.close()
        self.conn.close()
        return

    def start(self):
        self.gt_max_FAT()
        self.get_datas()
        self.insert_datas()
        self.del_datas()
        self.close_db()


if __name__ == "__main__":
    start = CrawInit()
    # start.del_datas()
    # start.get_datas()
    start.start()
    # start.insert_datas()
    # for data in start.rows:
    #     print(data)
    # start.gt_max_FAT()
