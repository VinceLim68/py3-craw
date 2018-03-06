import re
from urllib.parse import quote

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
# 一个小应用，判断一段文本中是否包含简体中：
contents = u'一个小应用，判断一段文本中是否包含简体中：'
contents = 'http://xm.58.com/ershoufang/?key=湖滨一里检察院宿舍'
match = zhPattern.search(contents)

if match:
    print(u'有中文：%s' % (match.group(0),))

else:
    print( u'没有包含中文')

comm_url = "http://xm.58.com/ershoufang/?key=" + quote('湖滨一里检察院宿舍', safe='/:?=')
print(comm_url)
print(quote(contents, safe='/:?='))
