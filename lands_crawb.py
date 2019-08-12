# coding:utf-8
import xlsxwriter
import Downloader
import re
from bs4 import BeautifulSoup


# reload(sys)
# sys.setdefaultencoding("utf-8")

# 爬取土地成交记录，并计算楼面地价

def crawland(url):
    downloader = Downloader.Downloader()
    html_cont,code = downloader.download(url)
    # html_cont = Downloader.Downloader.download(url)
    # print(html_cont)
    soup = BeautifulSoup(html_cont, 'html.parser',)
    records = soup.select("table.tab4 > tr")
    lands = []

    for record in records:
        data = {}
        r2 = record.select('td')  # 这里使用了再次解析
        data['landNo'] = (r2[0].contents[0].get('title'))
        data['href'] = (r2[0].contents[0].get('href'))
        data['use'] = (r2[1].contents[1].get('title'))
        data['address'] = (r2[2].contents[0].get('title'))
        data['date'] = (r2[3].get('title'))
        data['acreage'] = (r2[4].get('title'))

        if len(r2) == 8:  # 对于工业用地，缺少“建筑面积”一列
            data['floorArea'] = (r2[5].get('title'))
            data['price'] = (r2[6].get_text())
            data['user'] = (r2[7].get('title'))
        else:
            data['floorArea'] = data['acreage']
            data['price'] = (r2[5].get_text())
            data['user'] = (r2[6].get('title'))

        lands.append(data)

    return lands


def write_into_file(fout, name, lands):
    worksheet = fout.add_worksheet(name)

    title_format = fout.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': 'gray',
        'font_size': 12,
        'bg_color': 'silver'

    })

    title = ['地块编号', '地块用途', '土地位置', '成交日期', '土地面积', '建筑面积', '成交价', '受让人', '楼面价', '备注']
    worksheet.write_row('A1', title, title_format)

    # 设置冻结窗格
    worksheet.panes_frozen = True
    worksheet.freeze_panes(1, 1)

    url_format = fout.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': 'gray',
        'font_name': '楷体',
        'font_color': 'blue',
        'underline': True
    })

    format = fout.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': 'gray',
        'font_name': '楷体',
        'text_wrap': True  # 窗格内文本自动换行
    })

    format1 = fout.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': 'gray',
        'font_name': '楷体',
        'num_format': "0.00"
    })

    row = 1
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:G', 12)
    worksheet.set_column('H:H', 20)
    worksheet.set_column('I:I', 12)
    worksheet.set_column('J:J', 10)
    for land in lands:
        worksheet.write_url(row, 0, land['href'], url_format, land['landNo'])  # 写入超链接
        worksheet.write(row, 1, land['use'], format)
        worksheet.write(row, 2, land['address'], format)
        worksheet.write(row, 3, land['date'].split(' ')[0], format)
        worksheet.write(row, 4, land['acreage'], format)
        worksheet.write(row, 5, land['floorArea'], format)
        worksheet.write(row, 6, land['price'], format)
        worksheet.write(row, 7, land['user'], format)
        if get_price(land['price']) == 0 or get_area(land['floorArea']) == 0:
            pass
        else:
            worksheet.write(row, 8, get_price(land['price']) / get_area(land['floorArea']), format1)

        row += 1


def get_price(string):
    # price1 = 0
    # print(string)
    if not isinstance(string, str):string = string.decode()
    # print(string)
    if isinstance(string, str):
        if "万" in string:
            price1 = re.sub("\D", "", string.split('万')[0])
            price1 = float(price1) * 10000
        elif "亿" in string:
            price1 = re.sub("\D", "", string.split('亿')[0])
            price1 = float(price1) * 100000000
        else:
            price1 = myfilter(string)

    return price1


def get_area(string):
    sub = ['-', '地上总建筑面积', '＜', '≤', '低于', '小于']
    if not isinstance(string, str):string = string.decode()
    for item in sub:
        if item in string:
            string = string.split(item)[1]
            break
    return myfilter(string)


def myfilter(string):
    # 输入字符串
    # 从字符串中提取第一个连续的数字，其他忽略re.search(pattern, string[, flags])
    a = ""
    string = string.replace(',', '')  # 把千分位的数据改一下：1000,000=1000000
    for si in string:
        if si in "0123456789.":
            a += si
        elif a == "":
            continue
        else:
            break
    if a == "": a = "0"
    return float(a)


if __name__ == "__main__":
    # downloader = Downloader.Downloader()
    fout = xlsxwriter.Workbook('厦门出让土地汇总.xlsx')

    url = 'http://tz.xmtfj.gov.cn/jyjg_19.xhtml?a=&y='
    # url = ['http://tz.xmtfj.gov.cn/jyjg_19.xhtml?a=&y=']
    # data = downloader.download(url)
    # print(data)
    data = crawland(url)
    name = '经营性土地'
    write_into_file(fout, name, data)

    url = 'http://tz.xmtfj.gov.cn/jyjg_20.xhtml'
    data = crawland(url)
    name = '工业用地'
    write_into_file(fout, name, data)

    fout.close()
