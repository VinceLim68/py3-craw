import PageParser, ToolsBox, Downloader, re,AjkPage


class WbPage(AjkPage.AjkPage):

    #2021/1/25发现58同城与安居客的页面是同样的，所以直接继承过来
    def is_check(self, soup, type=1):
        # 判断是否是验证界面
        ischeck = soup.select("title")
        if len(ischeck) > 0:  # 如果找不到title,就认为不是验证界面
            title = ischeck[0].get_text().strip() if type == 2 else ischeck[0].text
            iscode = (title == "您所访问的页面不存在") or ("请输入验证码" in title)
        else:
            # iscode = False
            ischeck = soup.select("h1.item")
            if ischeck:
                title = ischeck[0].get_text().strip()
                iscode = True
            else:
                iscode = False

        if iscode:
            print('调试：页面标题是---->{0}'.format(title))

        return iscode

    def parse_datas(self, soup):
        page_data = self.parse_page(soup)
        for dic in page_data:
            dic['from'] = "58"
        return page_data



if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = WbPage()
    url = 'https://xm.58.com/ershoufang/p2/?from=esf,esf_list&PGTID=0d30000c-0025-ec8f-90bb-1364a7550ee7&ClickID=3'
    # url = 'https://xm.58.com/ershoufang/?key=%E7%89%B9%E6%88%BF%E9%93%B6%E6%BA%AA%E5%A2%85%E5%BA%9C(%E5%85%AC%E5%AF%93)%20-%20%E7%8E%AF%E4%B8%9C%E6%B5%B7%E5%9F%9F'
    # headers = dict(Host="xm.58.com", )
    html_cont, code = downloader.download(url)
    # print(html_cont)
    # print(type(html_cont))
    urls,datas = parser.page_parse(html_cont)
    # soup = parser.get_soup(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # ToolsBox.printDic(urls)
    ToolsBox.priList(datas)
