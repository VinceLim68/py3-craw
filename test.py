# import requests
# headers = {"User-Agent" : "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
# html = requests.get('http://esf.xm.fang.com/', headers=headers).text
# print(type(html))
# print(html)
data = '123  ,2,3,'
array1 = data.split(',')
print(len(array1[0].strip()))