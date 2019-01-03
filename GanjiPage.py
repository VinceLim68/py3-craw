import PageParser, ToolsBox, Downloader


class GanjiPage(PageParser.PageParser):
    def is_check(self, soup):
        # 判断是否是验证界面
        ischeck = soup.select("title")
        # print(ischeck)
        if len(ischeck) > 0:  # 如果找不到title,就认为不是验证界面
            title = ischeck[0].get_text().strip()
            # print(title)
            iscode = (title == "【在线客服】")
        else:
            iscode = False
        if iscode:
            print('调试：页面标题是---->{0}'.format(title))

        return iscode

    def parse_urls(self, soup):
        new_urls = set()
        # pagelinks = soup.select("ul.pageLink > li > a")
        pagelinks = soup.select(".pageBox > a")

        if pagelinks == None:
            print("本页面没有翻页链接。")
        else:
            for link in pagelinks:
                if link.has_attr('href'):
                    # new_urls.add("http://xm.ganji.com" + link['href'])
                    new_urls.add(link['href'])

        return new_urls

    def parse_datas(self, soup):

        page_datas = []

        details = soup.select(".size")
        # comms = soup.select("span.address-eara")
        prices = soup.select(".num")
        titles = soup.select("div.ershoufang-list .title a")
        regions = soup.select("span.area a")
        lists = soup.select(".ershoufang-list")

        for title, detail, list1, price, region in zip(titles, details, lists, prices, regions):
            # for title in titles:

            each_data = {'builded_year': 0, 'spatial_arrangement': '', 'floor_index': 0, 'total_floor': 0,
                         'advantage': '', 'title': title.get('title'), 'details_url': 'http:' + title.get('href')}
            for item in (detail.stripped_strings):
                d1 = self.parse_item(item)
                each_data = self.add_advantage(d1, each_data)

            each_data['total_price'] = ToolsBox.strToInt(price.get_text())

            address = list1.select("dd.address")

            # print(address[0])
            # print(len(address))
            if len(address) > 0:
                if len(address[0].select("a.address-eara")) > 0:
                    each_data['region'] = ToolsBox.clearStr(address[0].select("a.address-eara")[0].get_text())

                if len(address[0].select("span.address-eara")) > 0:
                    each_data['community_name'] = ToolsBox.clearStr(address[0].select("span.address-eara")[0].get_text())

            # try:
            # except (IndexError) as e:
            #     print("****页面数据不规范*****")
            #     input(address)

            # each_data['community_name'] = (comm.get_text())
            # print(comm.children)
            # for name in comm.descendants:
            #     print(name)
            #     # pass
            # print('-'*50)
            # each_data['region'] = ToolsBox.clearStr(region.get_text())

            each_data['from'] = "ganji"
            # print(each_data)
            each_data = self.pipe(each_data)
            #
            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        return page_datas


if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = GanjiPage()
    # url = 'http://xm.ganji.com/fang5/o2/'
    # url = 'http://xm.ganji.com/wblist/ershoufang/pn6/?key=%E5%A4%A9%E6%B9%96%E5%9F%8E%E5%A4%A9%E6%B9%96'
    # url = 'http://xm.ganji.com/wblist/ershoufang/pn8/?key=%E4%B8%80%E7%BA%BF%E6%B5%B7%E6%99%AF%E6%88%BF'
    url = 'http://xm.ganji.com/ershoufang/pn2/?key=%E5%9B%BD%E8%B4%B8%E8%93%9D%E6%B5%B7'
    headers = dict(Host="xm.ganji.com", Referer="http://xm.ganji.com/")
    html_cont = downloader.download(url, headers=headers)
    soup = parser.get_soup(html_cont)
    # print(parser.is_check(soup))
    # print(html_cont)
    urls, datas = parser.page_parse(html_cont)
    ToolsBox.priList(datas)
