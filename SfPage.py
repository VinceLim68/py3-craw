import PageParser,ToolsBox,Downloader
import bs4
from urllib import parse

class SfPage(PageParser.PageParser):

    def is_check(self,soup):
        # 判断是否是验证界面
        ischeck = soup.select("title")

        if len(ischeck) > 0:            #如果找不到title,就认为不是验证界面
            title = ischeck[0].get_text().strip()
            iscode = (title == "404 Not Found")
        else:
            iscode = False
        if iscode :
            print('调试：页面标题是---->{0}'.format(title))

        return iscode

    def print_title(self, soup):
        #for test
        #print the page's title
        title = soup.select("title")
        if len(title) > 0:
            print("The page's title is : {0}".format(title[0].get_text()))
        else:
            print("There is no title finded!")
        return

    def parse_urls(self, soup):
        new_urls = set()
        links = soup.select(".page_al span a")
        # links = soup.select("div.fanye > a")
        if links == None :
            print("本页面没有翻页链接。")
        else:
            for link in links:
                if link.get('href') != None:
                    new_urls.add("http://esf.xm.fang.com" + link.get('href'))
        return new_urls

    def parse_datas(self,soup):

        page_datas = []

        # title = soup.select("title")
        # if len(title) > 0:
        #     print("The page's title is : {0}".format(title[0].get_text()))
        # else:
        #     print("There is no title finded!")

        titles = soup.select(".shop_list > dl h4 a")
        houses = soup.select("p.tel_shop")
        comms = soup.select(".shop_list > dl dd p.add_shop a")
        comm_addresses = soup.select(".shop_list > dl dd p.add_shop span")
        prices = soup.select(".price_right .red b")
        for title,comm,comm_addresse ,house,price in zip(titles, comms,comm_addresses,houses,prices):
            each_data = dict(builded_year=0, spatial_arrangement='', floor_index=0, total_floor=0,
                              advantage='')

            each_data['title'] = title.get('title')
            each_data['details_url'] = "http://esf.xm.fang.com" + title.get('href')
            for item in house.children:
                if isinstance(item, bs4.element.NavigableString):
                    d1 = self.parse_item(ToolsBox.clearStr(item))
                    each_data = self.add_advantage(d1, each_data)


            each_data['community_name'] = comm.get('title').strip()
            each_data['community_address'] = comm_addresse.get_text().strip()
            each_data['comm_url'] = comm.get('href').strip()
            each_data['total_price'] = ToolsBox.strToInt(price.get_text())
            each_data['from'] = "Soufan"
        #
            each_data = self.pipe(each_data)
            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)


        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = SfPage()
    # comm = '泛华大厦'       #%b7%ba%bb%aa%b4%f3%cf%c3
    # print(parse.quote(comm, "gb2312"))
    # url = 'http://xm.esf.fang.com/house/c61-kw' + comm + '/'
    # url = "http://esf.xm.fang.com/house/i34/"
    url = "http://esf.xm.fang.com/house-xm2213064828/i32/"
    html_cont = downloader.download(url)
    print(html_cont)
    # if isinstance(html_cont, int) and (400 <= (html_cont) < 600):
    #     print(html_cont)
    # soup = parser.get_soup(html_cont)
    # parser.is_check(soup)
    # parser.print_title(soup)
    # urls,datas = parser.page_parse(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # ToolsBox.printDic(urls)
    # print(datas == 'checkcode')
    # ToolsBox.priList(datas)
    # ToolsBox.priList(urls)