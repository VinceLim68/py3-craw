import PageParser,ToolsBox,Downloader
import datetime
import traceback

class AjkPage(PageParser.PageParser):

    def is_check(self,soup):
        # 判断是否是验证界面
        ischeck = soup.select("title")

        if len(ischeck) > 0:            #如果找不到title,就认为不是验证界面
            title = ischeck[0].get_text().strip()
            iscode = ("访问验证-安居客" in title)
        else:
            iscode = False
        if iscode :
            print('调试：页面标题是---->{0}'.format(title))

        return iscode


    def parse_urls(self, soup):
        new_urls = set()
        pages = soup.select(".page-item>a")
        # pages = soup.find('div', class_='multi-page')
        if pages == None :
            print("本页面没有翻页链接。")
        else:
            for url in pages:
                link = url.get('href')
                if link != 'javascript:void(0);':new_urls.add(link)
        return new_urls

    def parse_test(self,soup):
        adds = soup.select('.property-content-info-comm-address')
        for add in adds:
            add_list =[]
            for string in add.strings:
                add_list.append(ToolsBox.clearStr(string.strip()))
            print(add_list)

            print("*"*50)


    def parse_page(self,soup):
        page_datas = []
        details_urls = soup.select(".property>a")
        titles = soup.select("h3.property-content-title-name")
        houses = soup.select("div.property-content-detail>section")
        # houses = soup.select('div.house-details')
        comms = soup.select('.property-content-info-comm-name')
        adds = soup.select('.property-content-info-comm-address')
        prices = soup.select('.property-price-total-num')
        for details_url,title, details, comm, price,add in zip(details_urls,titles, houses, comms, prices,adds):
            each_data = dict(advantage='', builded_year=0, spatial_arrangement='', floor_index=0, total_floor=0)
            each_data['title'] = title.get_text()
            each_data['details_url'] = details_url.get('href')

            houses = details.select(".property-content-info")
            detail = houses[0].select("p")
            for string in detail:
                d1 = self.parse_item(ToolsBox.clearStr(string.get_text().strip()))
                each_data = self.add_advantage(d1, each_data)

            each_data['community_name'] = comm.get_text().strip()

            add_list = []
            for string in add.strings:
                add_list.append(ToolsBox.clearStr(string.strip()))
            try:
                each_data['region'], each_data['block'], each_data['community_address'] = add_list
            except Exception as e:
                with open('logtest.txt', 'a+') as fout:
                    fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                    fout.write('AJK解析区、板块、地址时出错，待解析的数据：' )
                    traceback.print_exc(file=fout)
                    print(traceback.format_exc())
            # print(price)
            each_data['total_price'] = ToolsBox.strToInt(price.get_text())
            each_data['from'] = "AJK"
            # try:  # 2016.8.1 这里解析也时有出差，把它保留下来
            #     each_data['total_price'] = ToolsBox.strToInt(price.get_text())
            # except Exception as e:
            #     with open('logtest.txt', 'a+') as fout:
            #         fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
            #         fout.write('AJK解析total_price出错，待解析的数据：' + price.get_text())
            #         traceback.print_exc(file=fout)
            #         print(traceback.format_exc())

            # try:
            #     comminfo = comm.get('title').split()
            #     each_data['community_name'] = comminfo[0]
            #     each_data['region'], each_data['block'], each_data['community_address'] = comminfo[1].split('-', 2)
            # except Exception as e:
            #     with open('logtest.txt', 'a+') as fout:
            #         fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
            #         fout.write('Parse Failt of :%s \n' % comm.get('title'))
            #         traceback.print_exc(file=fout)
            #         print(traceback.format_exc())
            # each_data['community_name'] = each_data['community_name'].strip()

            # try:
            #     house = details.select('span')
            #     # 2016.8.17 重写了字段解析，抽象出一个parse_item方法
            #     for h in house:
            #         if len(h.attrs) == 0:
            #             string = h.get_text().encode('utf8')
            #             d1 = {}
            #             d1 = self.parse_item(string)
            #             each_data = self.add_advantage(d1, each_data)   #each_data = dict(each_data, **d1)
            #     each_data['from'] = "AJK"
            # except Exception as e:
            #     with open('logtest.txt', 'a+') as fout:
            #         fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
            #         fout.write('      待解析的数据：\n')
            #         for i1 in house:
            #             fout.write(str(i1) + '\n')
            #         fout.write('\n      字段数：' + str(len(house)) + '\n')
            #         traceback.print_exc(file=fout)
            #         print(traceback.format_exc())
            each_data = self.pipe(each_data)  # 2016.6.4增加一个专门的数据处理

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)
        return page_datas

    def parse_datas(self,soup):
        page_data = self.parse_page(soup)

        return page_data


if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = AjkPage()
    # url = 'https://xm.anjuke.com/sale/p1-rd1/?kw=%E8%8E%B2%E8%8A%B1%E4%B8%89%E6%9D%91%E7%A4%BE%E5%8C%BA&from_url=kw_final#filtersort'
    url = 'https://xm.anjuke.com/sale/?from=esf_list'
    headers = {
        "Host": "xm.anjuke.com",
        "Referer": "http://xm.anjuke.com/",
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
    }
    html_cont,code = downloader.download(url,headers=headers)
    # print(html_cont)
    # soup = BeautifulSoup(html_cont, 'lxml', from_encoding='urf-8')
    urls,datas = parser.page_parse(html_cont)
    # soup = parser.get_soup(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # parser.parse_test(soup)
    # print(datas)
    ToolsBox.priList(datas)