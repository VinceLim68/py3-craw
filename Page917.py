import PageParser,ToolsBox,Downloader

class www917Page(PageParser.PageParser):

    # def is_check(self,soup):
    #     # 判断是否是验证界面
    #     ischeck = soup.select("title")
    #
    #     if len(ischeck) > 0:            #如果找不到title,就认为不是验证界面
    #         title = ischeck[0].get_text().strip()
    #         iscode = (title == "访问验证-安居客")
    #     else:
    #         iscode = False
    #     if iscode :
    #         print('调试：页面标题是---->{0}'.format(title))
    #
    #     return iscode


    def parse_urls(self, soup):
        new_urls = set()
        pages = soup.select('.fanye1 > a')
        if pages == None :
            print("本页面没有翻页链接。")
        else:
            for url in pages:
                if 'javascript' not in url.get('href'):
                    new_urls.add(' http://www.917.com' + url.get('href'))
        return new_urls

    def parse_datas(self,soup):

        page_datas = []

        titles = soup.select('.title > a')
        items = soup.select('dd.info ')
        mores = soup.select('.moreInfo')
        prices = soup.select('.price')

        for title, item, price, more in zip(titles, items, prices, mores):
            each_data = dict(builded_year=0, spatial_arrangement='', floor_index=0, total_floor=0)
            each_data['title'] = title.get_text()
            each_data['details_url'] = 'http://www.917.com' + title.get('href')

            item1 = item.select('p')
            houseinfo = ToolsBox.clearStr(item1[1].get_text()).split('|')
            for temp in houseinfo:
                d1 = self.parse_item(temp.strip())
                if ('advantage' in each_data.keys()) and ('advantage' in d1.keys()):
                    d1['advantage'] = each_data['advantage'] + ',' + d1['advantage']
                each_data = dict(each_data, **d1)
                # print(temp)
            each_data['community_name'] = item1[2].select('a > span')[0].get_text()
            each_data['community_address'] = item1[2].select('span > a')[0].get_text()
            each_data['total_price'] = ToolsBox.strToInt(price.get_text())

            # 取面积
            d1 = self.parse_item(more.get_text())
            each_data = dict(each_data, **d1)

            each_data['from'] = "917"

            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)
        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = www917Page()
    url = 'http://www.917.com/sell/pn2/'
    headers = {
        "Host": "www.917.com",
        "Referer": "http://www.917.com/",
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
    }
    html_cont = downloader.download(url,headers=headers)

    urls,datas = parser.page_parse(html_cont)

    ToolsBox.priList(datas)