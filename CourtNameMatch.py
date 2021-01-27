import pandas as pd
import MatchID
matchid = MatchID.MatchID()
df = pd.read_excel(r'C:\Users\15007\Desktop\厦门地区基价.xlsx')
# print(df.columns)
# print(df.dtypes)
# column = list(df.columns.values)
# print(column)
# data=df.iloc[:,['基础小区表小区名称','房屋用途', '网络小区']].values#读所有行的title以及data列的值，这里需要嵌套列表
# print("读取指定行的数据：\n{0}".format(data))
# for item in df:
#     print(item)
# datas = df.loc[:,['基础小区表小区名称','房屋用途', '网络小区']]
# datas = list(datas)
# print(datas.loc[10,:])
df['基础小区表小区名称'].fillna('', inplace=True)
df['楼栋号(房屋名称)'].fillna('', inplace=True)
df['网络小区'].fillna('', inplace=True)
df['community_name'] = df['网络小区']
df['title'] = df['基础小区表小区名称'] + ',' + df['楼栋号(房屋名称)']+ ',' + df['网络小区']
# print(df.columns)
dfmiss = pd.DataFrame(columns = df.columns)
line_count=len(df)
column_num=0
dismiss_num = 0
for line_i in range(line_count):
    data = df.loc[line_i]
    column_num += 1
    getid = matchid.matchid(data)
    if getid == 0 :
        dismiss_num += 1
        # print('%s : the id is %s'%(column_num,getid))
        dfmiss = dfmiss.append(data, ignore_index=True)
print('no match number is %s'%dismiss_num)
print(dfmiss)
dfmiss.to_excel(r'C:\Users\15007\Desktop\1.xlsx')
# ,[思明]前埔柯厝路362-378号,源泉山庄(车位)