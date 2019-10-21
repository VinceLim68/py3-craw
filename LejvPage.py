import PageParser,ToolsBox,Downloader

class LejvPage(PageParser.PageParser):

    def parse_urls(self, soup):
        new_urls = set()
        pagelinks = soup.select("div.page > a")
        if pagelinks == None:
            print("本页面没有翻页链接。")
        else:
            for link in pagelinks:
                if link.has_attr('href'): new_urls.add('http:'+link['href'])
        return new_urls

    def parse_datas(self,soup):

        page_datas = []

        # details = soup.select("div.house-info")
        # comms = soup.select("div.house-info > a ")
        # positions = soup.select("div.house-position")
        # prices = soup.select("span.georgia")
        # titles = soup.select("h3 > a")
        # regions = soup.select(".region")

        # for title,comm,detail,position,price,region in zip(titles,comms,details,positions,prices,regions):

        # 2019/9/9乐居网改版面的
        titles = soup.select("div.title_in")
        d_urls = soup.select("div.title_in > a")
        adds = soup.select("div.address")
        infos = soup.select("div.house_info")
        prices = soup.select("div.price > span")
        for title,add,d_url,info,price in zip(titles,adds,d_urls,infos,prices):
            each_data = dict(builded_year=0, spatial_arrangement='', floor_index=0, total_floor=0,
                             title=title.get('title'))
            comms = add.select('span')
            each_data['community_name'] = ToolsBox.clearStr(comms[0].get_text())
            for comm in comms:
                comm = ToolsBox.clearStr(comm.get_text())
                if '-' != comm:
                    if '-' in comm:
                        c_item = comm.split('-')
                        each_data['region'] = c_item[0]
                        each_data['block'] = c_item[1]
                    if '年' in comm:
                        out = self.parse_item(comm)
                        each_data = self.add_advantage(out,each_data)
            h_info = info.select('span')
            for item in h_info:
                item = ToolsBox.clearStr(item.get_text())
                each_data = self.add_advantage(self.parse_item(item), each_data)
            each_data['details_url'] = 'https:' + d_url.get('href')
            each_data['total_price'] = ToolsBox.strToInt(price.get_text())

            # , details_url='http://xm.esf.leju.com' + title.get('href')
            # mr20 = detail.select("span.mr20")
            # posi = position.select("span")
            # for j in range(1,len(posi)):
            #     out = self.parse_item(posi[j].get_text())
            #     each_data = self.add_advantage(out, each_data)
            #     # if len(out) > 0:
            #     #     if ('advantage' in each_data.keys()) and ('advantage' in out.keys()):
            #     #         each_data['advantage'] = each_data['advantage'] + ',' + out['advantage']
            #     #     else:
            #     #         each_data = dict(each_data, **out)
            # for item in mr20:
            #     d1 = self.parse_item(item.get_text())
            #     each_data = self.add_advantage(d1, each_data)
            #     # if len(d1) > 0:
            #     #     if ('advantage' in each_data.keys()) and ('advantage' in d1.keys()):
            #     #         each_data['advantage'] = each_data['advantage'] + ',' + d1['advantage']
            #     #     else:
            #     #         each_data = dict(each_data, **d1)
            # each_data['community_address'] = region.get_text().strip()
            # each_data['community_name'] = comm.get_text()
            # each_data['total_price'] =ToolsBox.strToInt(price.get_text())
            # each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)

            each_data['from'] = "lejv"
            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = LejvPage()
    url = 'https://xm.esf.leju.com/house'
    headers = {
        "Host": "xm.esf.leju.com",
        "Referer": "http://xm.esf.leju.com/house/",
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
    }

    html_cont,code = downloader.download(url,headers=headers)
    # print(html_cont)
    urls,datas = parser.page_parse(html_cont)
    ToolsBox.priList(datas)