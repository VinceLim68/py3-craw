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
                    new_urls.add(' https://www.917.com' + url.get('href'))
        return new_urls

    def parse_datas(self,soup):

        page_datas = []

        items = soup.select('div.info')
        titles = soup.select('p.title a ')
        comms = soup.select('p.hlistP  a span')
        addresses = soup.select('p.hlistP a.addressChange')
        regions = soup.select('p.hlistP > span')
        mores = soup.select('.moreInfo')
        prices = soup.select('.price')

        for item,title,comm,addr,region,price,more in \
                zip(items,titles,comms,addresses,regions,prices,mores):

            each_data = dict(builded_year=0, spatial_arrangement='', floor_index=0, total_floor=0)

            each_data['title'] = title.get_text()
            each_data['details_url'] = 'http://www.917.com' + title.get('href')

            details = item.select('p')
            for string in details[1].stripped_strings:
                d1 = self.parse_item(string.strip())
                each_data = self.add_advantage(d1, each_data)

            each_data['community_name'] = comm.get_text()
            each_data['community_address'] = addr.get_text()
            each_data['region'] = region.get_text().replace('|', '').replace(' ','')
            each_data['total_price'] = ToolsBox.strToInt(price.get_text())
            each_data['from'] = "917"

            getP = more.select('p')
            for p in getP:
                if '建筑面积' in p.get_text():
                    d1 = self.parse_item(p.get_text().strip())
                    each_data = self.add_advantage(d1, each_data)

            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)
        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = www917Page()
    url = 'https://www.917.com/sell/pn10/'
    headers = {
        "Host": "www.917.com",
        "Referer": "http://www.917.com/",
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
    }
    html_cont = downloader.download(url,headers=headers)

    urls,datas = parser.page_parse(html_cont)

    ToolsBox.priList(urls)