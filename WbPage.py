import PageParser, ToolsBox, Downloader, re


class WbPage(PageParser.PageParser):
    def is_check(self, soup, type=1):
        # 判断是否是验证界面
        ischeck = soup.select("title")

        if len(ischeck) > 0:  # 如果找不到title,就认为不是验证界面
            title = ischeck[0].get_text().strip() if type == 2 else ischeck[0].text
            iscode = (title == "您所访问的页面不存在") or (title == "请输入验证码")
        else:
            iscode = False
        if iscode:
            print('调试：页面标题是---->{0}'.format(title))

        return iscode

    def parse_urls(self, soup):
        new_urls = set()
        pages = soup.select('.pager > a')
        if pages == None:
            print("本页面没有翻页链接。")
        else:
            for link in pages:
                if 'http://xm.58.com' in link.get('href'):
                    new_urls.add(link.get('href'))
                else:
                    new_urls.add('http://xm.58.com' + link.get('href'))
        return new_urls

    def parse_datas(self, soup):

        page_datas = []
        # print(soup)

        titles = soup.select("h2.title > a")
        prices = soup.select('p.sum > b')
        houses = soup.select('.list-info')

        for title, price, house in zip(titles, prices, houses):
            each_data = {'advantage': '', 'builded_year': 0, 'spatial_arrangement': '', 'floor_index': 0,
                         'total_floor': 0, 'title': title.get_text(), 'details_url': title.get('href'),
                         'total_price': ToolsBox.strToInt(price.get_text())}
            details = house.select('p.baseinfo')
            spans = details[0].select('span')
            for span in spans:
                string = ToolsBox.clearStr(span.get_text()).encode('utf8')
                # d1 = {}
                d1 = self.parse_item(string)
                each_data = self.add_advantage(d1, each_data)  # each_data = dict(each_data, **d1)
            comms = details[1].select('a')

            each_data['community_name'] = comms[0].get_text()

            if comms[0].get('href') is None:
                each_data['comm_url'] = ''
            else:
                each_data['comm_url'] = 'http://xm.58.com' + comms[0].get('href')

            each_data['from'] = "58"

            try:
                if len(comms) >= 2:
                    # input('region')
                    each_data['region'] = comms[1].get_text().strip()
            except Exception as e:
                # print('-------这个记录没有拿到小区的区域------------')
                # ToolsBox.printDic(each_data)
                print(e)

            try:
                if len(comms) >= 3:
                    # input('address')
                    each_data['community_address'] = comms[2].get_text().strip()
            except Exception as e:
                # print('-------这个记录没有拿到小区地址------------')
                # ToolsBox.printDic(each_data)
                print(e)

            each_data = self.pipe(each_data)

            if each_data:
                match_comm = re.findall(r'^\d+$', each_data['community_name'])
                # 不知道为什么，有时小区名称会都是数字，需要屏蔽
                # print(match_comm)
                if len(match_comm) > 0:
                    print('/////////////////出现纯数字的小区了!!!!!!////////////////////////')
                    ToolsBox.priList(each_data)
                    # print(each_data['community_name'])
                    var1 = input(each_data['community_name']+'出现纯数字的小区了!!!!!!!!!')
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        return page_datas


if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = WbPage()
    url = 'https://xm.58.com/ershoufang/?key=%E7%89%B9%E6%88%BF%E9%93%B6%E6%BA%AA%E5%A2%85%E5%BA%9C(%E5%85%AC%E5%AF%93)%20-%20%E7%8E%AF%E4%B8%9C%E6%B5%B7%E5%9F%9F'
    headers = dict(Host="xm.58.com", )
    html_cont, code = downloader.download(url, headers=headers)
    # print(html_cont)
    # print(type(html_cont))
    urls,datas = parser.page_parse(html_cont)
    # soup = parser.get_soup(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # ToolsBox.printDic(urls)
    ToolsBox.priList(datas)
