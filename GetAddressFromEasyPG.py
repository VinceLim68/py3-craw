import pymssql
import pymysql
import MatchID
import re
import datetime
import traceback

# 从EasyPG里取出小区和地址的信息，导入询价系统的后台地址库中去
conn = pymssql.connect(
    server = '192.168.1.250',
    user = 'sa',
    password = 'siwing',
    database = 'EasyPG',
    charset="utf8")
cursor = conn.cursor(as_dict=True)
sql = """
    SELECT 
    xqkid,
    CONVERT(nvarchar(100), fwlp) fwlp,
    CONVERT(nvarchar(100), fwdy) fwdy,
    CONVERT(nvarchar(100),b.xqName) xqName,
    CONVERT(nvarchar(100),a.xqName) xqName1,
    CONVERT(nvarchar(100),dz) title,
    cjdj,
    cjAmt,
    jzmj,
    CONVERT(nvarchar(100),pgyt) pgyt,
    CONVERT(nvarchar(100),dt) dt,
    zcs,
    cc,
    jcnf,
    CONVERT(nvarchar(100),jzjg) jzjg,
    CONVERT(nvarchar(100),city) city
    FROM PG_SE_Gjxmdetail A 
    LEFT JOIN PG_SE_Xqzdk b on a.xqkid = b.KID
"""

insertsql = """
    INSERT INTO commaddress (
    comm_id,
    comm_name,
    address,
    city,
    region,
    road,
    doorplate,
    type,
    buildYear,
    floors,
    elevator,
    structure
    ) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

findsql = """
    SELECT
    id,
    comm_id ,
    comm_name,
    address,
    city,
    region,
    road,
    doorplate,
    type,
    buildYear,
    floors,
    elevator,
    structure
    from commaddress WHERE 
    commaddress.comm_id = %s
    AND commaddress.road = %s
    AND commaddress.doorplate = %s
"""

updatesql = """
    UPDATE commaddress
    SET 
    comm_id = %s,
    comm_name = %s,
    address = %s,
    city = %s,
    region = %s,
    road = %s,
    doorplate = %s,
    type = %s,
    buildYear = %s,
    floors = %s,
    elevator = %s,
    structure = %s
    WHERE id = %s;
"""
pattern = '(.*市)?(.*区)?(\D*)(\d*)(-\d+)?号(之[三二一四五六七八九十]*)?(\D*)?(\d+)?(室|单元|号车位)?'

updatenum = 0   #更新的记录数
addnum = 0      #增加的记录数

cursor.execute(sql)
rows = cursor.fetchall()
# print(len(rows))

matchid = MatchID.MatchID()
for data in rows:
    if data['xqName1']:
        data['community_name'] = data['xqName1']
    else:
        data['community_name'] = data['xqName']
    if data['community_name']:          #有小区名才能去匹配小区id
        commid = matchid.matchid(data)
        if commid > 999:                #匹配小区id成功才取数据
            matchdz = re.match(pattern, data['fwlp'])
            if matchdz:                 #解析地址成功才存入询价系统的后台地址库
                try:
                    region = matchdz.group(2) if matchdz.group(2) else ''
                    matchid.cursor.execute(findsql, (commid, matchdz.group(3), matchdz.group(4) + '号'))
                    findrows = matchid.cursor.fetchall()
                    if findrows:
                        thisitem = [
                            commid,
                            data['community_name'] if data['community_name']!='' else findrows[0]['comm_name'],
                            data['title'] if data['title']!='' else findrows[0]['address'],
                            data['city'] if data['city']!='' else findrows[0]['city'],
                            region if region!='' else findrows[0]['region'],
                            matchdz.group(3) if matchdz.group(3)!='' else findrows[0]['road'],
                            matchdz.group(4) + '号' if matchdz.group(4)!='' else findrows[0]['doorplate'],
                            data['pgyt']  if data['pgyt']!='' else findrows[0]['type'],
                            datetime.datetime.strptime(data['jcnf'], '%Y') if data['jcnf']!='' and data['jcnf'] is not None else findrows[0]['buildYear'],
                            data['zcs'] if data['zcs']!='' else findrows[0]['floors'],
                            data['dt'] if data['dt']!='' else findrows[0]['elevator'],
                            data['jzjg'] if data['jzjg']!='' else findrows[0]['structure'],
                            findrows[0]['id']
                        ]
                        matchid.cursor.execute(updatesql,thisitem)
                        updatenum += 1
                        print('更新:{0}:{1}-{2},共{3}层,{4}年,{5}'.format(data['community_name'],matchdz.group(3),matchdz.group(4)+'号',data['zcs'],data['jcnf'],updatenum))
                    else:
                        jcnf = datetime.datetime.strptime(data['jcnf'], '%Y') if data['jcnf'] is not None else None
                        thisitem = [commid, data['community_name'], data['title'], data['city'], region, matchdz.group(3),
                                    matchdz.group(4) + '号', data['pgyt'], jcnf,
                                    data['zcs'] if data['zcs']!='' else None, data['dt'], data['jzjg']]
                        matchid.cursor.execute(insertsql,thisitem)
                        addnum += 1
                        print('新增:{0}:{1}-{2},共{3}层,{4}年,{5}'.format(data['community_name'],matchdz.group(3),matchdz.group(4)+'号',data['zcs'],data['jcnf'],addnum))
                    matchid.db.commit()
                except pymysql.err.DataError as e:
                    code, message = e.args
                    print(code, message)
                    print(findrows)
                    print(data)
                    input(thisitem)
                except pymysql.err.InternalError as e:
                    code, message = e.args
                    print(code, message)
                    print(findrows)
                    print(data)
                    input(thisitem)

print('共修改{0}个记录，增加{1}个记录'.format(updatenum,addnum))



