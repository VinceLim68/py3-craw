import pymssql
import pymysql
import datetime
import traceback
mysqlconn = pymysql.connect(host="office.xmcdhpg.cn", user="root",
                                passwd="root", db="property_info",
                                charset="utf8", port=6153)
mysqlcur = mysqlconn.cursor(cursor=pymysql.cursors.DictCursor)

# 从业务系统里取数据
conn = pymssql.connect('192.168.1.3:5433','sa','sa','Evalue')
cursor = conn.cursor(as_dict=True)
cursor.execute("SELECT RAddress,pa_locatedregion FROM C_PGRecord "
               "Where pa_locatedregion is not NULL AND pa_locatedregion<>''" )

# rows = cursor.fetchall()
#
# dupli = 0       #计数：插入数据库时的重复记录值
# success = 0     #计数：插入数据库的成功记录数量
# sql = """
#             INSERT commaddress (address,comm_name) VALUES (%s,%s)
#         """
# for data in rows:
#     try:
#         mysqlcur.execute(sql,(data['RAddress'],data['pa_locatedregion']))
#         success = success + 1
#         mysqlconn.commit()
#         print(success)
#     except pymysql.err.IntegrityError as e:
#         if e.args[0] == 1062 :
#             dupli = dupli + 1
#         else:
#             with open('logtest.txt','a+') as fout:
#                 fout.write(str(datetime.datetime.now()) + 'record by CrawInit \n')
#                 traceback.print_exc(file=fout)
#             print(traceback.format_exc())
#             code, message = e.args
#             print(code,message)
#     except pymysql.err.InternalError as e:
#         with open('logtest.txt','a+') as fout:
#             fout.write(str(datetime.datetime.now()) + 'record by CrawInit \n')
#             traceback.print_exc(file=fout)
#             print(traceback.format_exc())
#         code, message = e.args
#         print(code,message)
#     except:
#         print("{0},{1}".format(data['RAddress'],data['pa_locatedregion']))
#
# print("本次共{0}个数据，存入{1},重复{2}".format(len(rows),success,dupli))

# 从撰稿系统里取数据
apprsal_cdh_conn = pymysql.connect(host="192.168.1.207", user="root",
                                passwd="root", db="apprsal_cdh",
                                charset="utf8")
apprsal_cdh_cur = apprsal_cdh_conn.cursor(cursor=pymysql.cursors.DictCursor)
apprsal_cdh_cur.execute("SELECT PA_Located,PA_YearBuilt,PA_Structure,"
            "PA_Layers,PA_LocatedRegion,PA_Elevator FROM T_PROPTY_TOBE_APPRSAL "
            "Where PA_LocatedRegion is not NULL AND pa_locatedregion<>''" )
apprsal_cdh_rows = apprsal_cdh_cur.fetchall()

dupli = 0       #计数：插入数据库时的重复记录值
success = 0     #计数：插入数据库的成功记录数量
sql = """
            INSERT commaddress (address,comm_name,buildYear,structure,floors,elevator) 
            VALUES (%s,%s,%s,%s,%s,%s)
        """
for data in apprsal_cdh_rows:
    if data['PA_Layers']=='':data['PA_Layers']=0
    try:
        mysqlcur.execute(sql,(data['PA_Located'],data['PA_LocatedRegion'],
                              data['PA_YearBuilt'],data['PA_Structure'],
                              data['PA_Layers'],data['PA_Elevator']))
        success = success + 1
        mysqlconn.commit()
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
    except:
        print("{0},{1}".format(data['PA_Located'],data['PA_LocatedRegion']))

print("本次共{0}个数据，存入{1},重复{2}".format(len(apprsal_cdh_rows),success,dupli))

