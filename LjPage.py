import PageParser,ToolsBox,Downloader
import re

class LjPage(PageParser.PageParser):

    def is_check(self,soup):
        # 判断是否是验证界面
        ischeck = soup.select("title")
        if len(ischeck) > 0:            # 如果找不到title,就认为不是验证界面
            title = ischeck[0].get_text().strip()
            iscode = title == "验证异常流量-链家网"
        else:
            iscode = False

        if iscode :
            print('调试：页面标题是---->{0}'.format(title))
        return iscode

    def parse_urls(self, soup):
        new_urls = set()
        # 链家不管是否有翻页，都有这个类
        links = soup.select("div.house-lst-page-box")
        if links:
            t_page = eval(links[0].get('page-data'))['totalPage']
            url = links[0].get('page-url')
            print(url)
            for i in range(1, t_page + 1):
                new_urls.add("https://xm.lianjia.com" + url.replace("{page}", str(i)))
        else:
            print("本页没有翻页链接")
        # ToolsBox.priList(new_urls)
        return new_urls

    def parse_datas(self,soup):
        page_datas = []

        titles = soup.select("div.title > a")
        houseinfo = soup.select("div.houseInfo")
        positionInfo = soup.select("div.positionInfo")
        totalprices = soup.select("div.totalPrice")
        #
        for title, info, position, totalPrice in zip(titles, houseinfo, positionInfo, totalprices):
            each_data = {'builded_year': 0, 'spatial_arrangement': '', 'floor_index': 0, 'total_floor': 0}
            each_data['title'] = title.get_text()
            each_data['details_url'] = title.get('href')
            each_data['total_price'] = ToolsBox.strToInt(totalPrice.get_text())

            info_item = info.get_text().split('|')

            # each_data['community_name'] = info_item[0].strip()  # 第1个总是小区名称
            for i in range(0, len(info_item)):
                d1 = self.parse_item(info_item[i].strip())
                each_data = self.add_advantage(d1,each_data)

            position = position.get_text().replace('\t', '').replace('\n', '').split()
            each_data['community_name'] = position[0].strip()  # 10月21日改变了小区名称位置
            # print(position)
            each_data['block'] = position[-1]

            if ')' not in position[0]:  # 链前的别墅会用'4层2008年建'的形式，加入')'，以便分隔
                position[0] = position[0].replace('层', '层)')

            for item in position[0].split(')'):  # 2017.4.1链家格式有改
                d1 = self.parse_item(item.strip())  # 2017.4.1链家格式有改
                each_data = self.add_advantage(d1, each_data)
                # each_data = dict(each_data, **d1)

            each_data['from'] = "lianjia"

            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        if not page_datas:
            total_num = soup.select('.total span')
            if total_num:
                page_datas = total_num[0].get_text().strip()
        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = LjPage()
    # url ="https://xm.lianjia.com/ershoufang/rs%E5%90%8C%E5%AE%89%E5%A4%A7%E5%94%90%E4%B8%96%E5%AE%B6%E4%B8%80%E3%80%81%E4%BA%8C%E6%9C%9F/"
    url ="https://xm.lianjia.com/ershoufang/rs%E5%90%8C%E5%AE%89%E5%A4%A7%E5%94%90%E4%B8%96%E5%AE%B6%E4%B8%80%E3%80%81%E4%BA%8C%E6%9C%9F/"
    headers = {"Host": "xm.lianjia.com",
               "Referer": "https://xm.lianjia.com/ershoufang/",
               "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    html_cont,code = downloader.download(url,headers=headers)
    # print((html_cont))
    urls,datas = parser.page_parse(html_cont)
    # soup = parser.get_soup(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # ToolsBox.printDic(urls)
    print(datas)
    # ToolsBox.priList(datas)
    # ToolsBox.priList(urls)