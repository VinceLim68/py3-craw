import PageParser,ToolsBox,Downloader
import datetime
import traceback

class DanxiaPage(PageParser.PageParser):

    def parse_urls(self, soup):
        new_urls = set()
        pagelinks = soup.select('a.num')

        if pagelinks == None:
            print("本页面没有翻页链接!!")
        else:
            for link in pagelinks:
                if link.get('href') != None:
                    new_urls.add('https://danxia.com' + link.get('href'))
        return new_urls


    def parse_datas(self,soup):

        page_datas = []

        titles = soup.select("h2.fix a")
        houses = soup.select('p.moudle')
        houses1 = soup.select('td.sm222 p.msg')
        # comms = soup.select('span.comm-address')
        prices = soup.select('div.percent b')
        # print(titles)
        for title,detail,detail1,price in zip(titles,houses,houses1,prices):
            # each_data = {}
            each_data = dict(advantage='', builded_year=0, spatial_arrangement='', floor_index=0, total_floor=0)
            each_data['title'] = title.get_text()
            each_data['details_url'] = 'https://danxia.com' + title.get('href')

            each_data['community_name'] = detail.select('a')[0].get_text()
            temp = detail.select('span')
            for item in temp:
                d1 = self.parse_item(item.get_text())
                each_data = dict(each_data, **d1)

            temp1 = detail1.select('span')
            for item in temp1:
                d1 = self.parse_item(item.get_text())
                each_data = dict(each_data, **d1)

            each_data['total_price'] = ToolsBox.strToInt(price.get_text())

            each_data['from'] = "Danxia"

            each_data = self.pipe(each_data)  # 2016.6.4增加一个专门的数据处理

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        return page_datas
        # return each_data
if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = DanxiaPage()
    url = 'https://danxia.com/house/all/PG2'
    headers = {
        "Referer": "https://danxia.com/house/all",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    html_cont = downloader.download(url,headers=headers)
    soup = parser.get_soup(html_cont)
    # datas = parser.parse_datas(soup)
    # print(datas)
    urls,datas = parser.page_parse(html_cont)
    for data in urls:
        print('='*50)
        ToolsBox.printDic(data)