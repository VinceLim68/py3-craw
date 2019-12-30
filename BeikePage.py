import PageParser,ToolsBox,Downloader,re
import json

class BeikePage(PageParser.PageParser):

    def parse_urls(self, soup):
        new_urls = set()
        pagelinks = soup.select(".house-lst-page-box")

        if len(pagelinks) == 0:
            print("本页面没有翻页链接。")
        else:
            page_url = 'https://xm.ke.com' + pagelinks[0].get('page-url')
            page = json.loads(pagelinks[0].get('page-data'))
            totalpage = page['totalPage']
            i = 1
            while i <= totalpage:
                new_urls.add(page_url.replace('{page}',str(i)))
                i += 1

        return new_urls

    def parse_datas(self,soup):

        page_datas = []

        details = soup.select(".houseInfo")
        # comms = soup.select(".houseInfo > a ")
        comms = soup.select(".positionInfo a")
        # regions = soup.select(".positionInfo a  ")
        # ToolsBox.priList(details)
        # positions = soup.select("div.positionInfo")
        prices = soup.select(".totalPrice")
        titles = soup.select("div.title a.CLICKDATA")

        # for title,comm,detail,position,price,region in zip(titles,comms,details,positions,prices,regions):
        for title,detail,price,comm in zip(titles,details,prices,comms):
            each_data = dict(builded_year=0, spatial_arrangement='', floor_index=0, total_floor=0,
                             details_url=title.get('href'), advantage='')
            each_data['title'] = title.get_text().strip()

            # houseInfos = ToolsBox.clearStr(detail.get_text()).split('|')
            houseInfos = re.split(r'\s*[|,\s]\s*',ToolsBox.clearStr(detail.get_text()))
            # ToolsBox.priList(houseInfos)
            # each_data['community_name'] = houseInfos[0]
            each_data['community_name'] = comm.get_text().strip()
            if len(each_data['community_name']) >= 20:
                input(each_data['community_name'] + ':' + str(len(each_data['community_name'])))


            # houseInfos = houseInfos[1:]         #第一个是小区名称，切片去除
            for item in houseInfos:
                d1 = self.parse_item(item)
                each_data = self.add_advantage(d1, each_data)


            each_data['total_price'] = ToolsBox.strToInt(price.get_text())
            each_data['from'] = "Beike"
            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)
            # print(each_data)
        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = BeikePage()
    # url = ' https://xm.ke.com/ershoufang/pg1rs嘉源新城（53、55、57）'
    url = 'https://xm.ke.com/ershoufang/pg2/'
    html_cont,code = downloader.download(url)
    soup = parser.get_soup(html_cont)
    urls,datas = parser.page_parse(html_cont)
    ToolsBox.priList(datas)
    # ToolsBox.priList(urls)
