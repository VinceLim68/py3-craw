from bs4 import BeautifulSoup
import LjPage,ToolsBox,Downloader

class LjCommPrice(LjPage.LjPage):
    def parse_datas(self, soup):
        totalfind = soup.select("h2.total.fl > span")
        if 0 == ToolsBox.strToInt(totalfind[0].get_text()):return '0'
        page_datas = []
        communitys = soup.select("div.info>div.title>a")
        regions = soup.select('a.district')
        blocks = soup.select('a.bizcircle')
        prices = soup.select('.totalPrice>span')
        forsales = soup.select('.totalSellCount>span')
        buildyears = soup.select('.positionInfo')

        for community, region, block, price,forsale,buildyear in zip(communitys, regions, blocks, prices,forsales,buildyears):
            each_data = dict()
            each_data['community_name'] = community.get_text()
            each_data['community_url'] = community.get('href')
            each_data['region'] = region.get_text()
            each_data['block'] = block.get_text()
            each_data['builded_year'] = ToolsBox.strToInt(buildyear.get_text())
            each_data['forsale_num'] = ToolsBox.strToInt(forsale.get_text())
            each_data['price'] = ToolsBox.strToInt(price.get_text())
            # each_data['date']
            each_data['from'] = "LJ"
            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)
            # ToolsBox.printDic(page_datas)

        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = LjCommPrice()
    # url ="https://xm.lianjia.com/ershoufang/rs%E5%90%8C%E5%AE%89%E5%A4%A7%E5%94%90%E4%B8%96%E5%AE%B6%E4%B8%80%E3%80%81%E4%BA%8C%E6%9C%9F/"
    url ="https://xm.lianjia.com/xiaoqu/pg1rs%20%E6%98%8E%E5%8F%91%E5%8D%8A%E5%B2%9B%E7%A5%A5%E6%B9%BE/"
    headers = {"Host": "xm.lianjia.com",
               "Referer": "https://xm.lianjia.com/ershoufang/",
               "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    html_cont,code = downloader.download(url,headers=headers)
    # print((html_cont))
    soup = BeautifulSoup(html_cont, "lxml")
    datas = parser.parse_datas(soup)
    # soup = parser.get_soup(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # ToolsBox.printDic(urls)
    ToolsBox.priList(datas)
