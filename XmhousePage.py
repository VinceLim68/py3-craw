import PageParser,ToolsBox,Downloader
import datetime
import traceback
import re
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
from bs4 import BeautifulSoup

class XmhousePage(PageParser.PageParser):

    def is_check(self,soup):
        # 判断是否是验证界面
        ischeck = soup.select("title")

        if len(ischeck) > 0:            #如果找不到title,就认为不是验证界面
            title = ischeck[0].get_text().strip()
            iscode = (title == "服务器安全狗防护验证页面")
        else:
            iscode = False
        if iscode :
            print('调试：页面标题是---->{0}'.format(title))

        return iscode

    def parse_urls(self, soup):
        new_urls = set()

        urls = soup.select(".pageBlue > a")
        if  urls == None :
            print("本页面没有翻页链接")
        else:
            for url in urls:
                if url.has_attr('href'):
                    new_urls.add('http://esf.xmhouse.com' + url['href'])
            # ToolsBox.priList(new_urls)
        return new_urls

    def parse_datas(self,soup):
        i = 1
        page_datas = []

        details = soup.select('dd.detail ')
        hrefs = soup.select('span.c_blue0041d9.aVisited.f14B > a')
        comms = soup.select('span.xuzhentian > a')
        prices = soup.select('span > em')

        for detail, href, comm, price in zip(details, hrefs, comms, prices):

            each_data = dict(advantage='', builded_year=0, spatial_arrangement='', floor_index=0, total_floor=0)
            each_data['title'] = href.get_text().strip()
            each_data['community_name'] = comm.get_text().strip()
            each_data['details_url'] = "http://esf.xmhouse.com" + href.get('href')
            each_data['total_price'] = ToolsBox.strToInt(price.get_text())
            h_infos = re.search(r'<span style="margin-left: 5px; color: #000000">.*</span>(.*) <div', str(detail), re.S) \
                .group(1).replace('<br/>', '').replace('\r\n', '').replace(' ', '').split('，')

            for item in h_infos:
                try:
                    d1 = {}
                    d1 = self.parse_item(item)
                    each_data = self.add_advantage(d1, each_data)   #each_data = dict(each_data, **d1)
                except Exception as e:
                    with open('logtest.txt', 'a+') as fout:
                        fout.write('*************' + str(datetime.datetime.now()) + '*************\n')
                        fout.write('      获取的数据：')
                        for i1 in h_infos:
                            fout.write(i1 + ',')
                        fout.write('\n      XmParser解析时发生错误的Item是： ' + str(item) + '\n')
                        traceback.print_exc(file=fout)
                        print(traceback.format_exc())


            each_data['from'] = "XMHouse"
            # ToolsBox.printDic(each_data)
            # print('******************{0}******************'.format(i))
            # i += 1

            each_data = self.pipe(each_data)
            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        return page_datas


if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = XmhousePage()
    url = 'http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_2.html'
    html_cont,code = downloader.download(url)
    # html_cont = unicode(html_cont,'gbk')
    # print((html_cont))
    # soup = parser.get_soup(html_cont)
    # urls, datas = parser.page_parse(html_cont)
    # print(html_cont)
    urls,datas = parser.page_parse(html_cont)
    # datas = parser.parse_datas(soup)
    # urls = parser.parse_urls(soup)
    # ToolsBox.printDic(urls)
    ToolsBox.priList(urls)
    # print(datas)
    # print(urls)