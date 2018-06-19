import PageParser,ToolsBox,Downloader
import json

class BeikePage(PageParser.PageParser):

    def parse_urls(self, soup):
        new_urls = set()
        pagelinks = soup.select(".house-lst-page-box")
        # print(len(pagelinks))
        # print(pagelinks[0].get('page-data'))
        # print(page['totalPage'])

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
        comms = soup.select(".houseInfo > a ")
        regions = soup.select(".positionInfo a  ")
        # ToolsBox.priList(details)
        positions = soup.select(".positionInfo")
        prices = soup.select(".totalPrice span")
        titles = soup.select("div.title a.CLICKDATA")

        for title,comm,detail,position,price,region in zip(titles,comms,details,positions,prices,regions):
            each_data = dict(builded_year=0, spatial_arrangement='', floor_index=0, total_floor=0,
                             details_url=title.get('href'))
            each_data['community_name'] = comm.get_text()
            each_data['title'] = title.get_text().strip()
            each_data['region'] = region.get_text().strip()
            # print(each_data['region'])

            # 这是第二行的数据，主要是放建成年份和楼层
            temp = position.contents[1]
            # print(temp)
            # 防止格式不完全是“高楼层(共7层)2006年建板塔结合 ”，
            # 有时是“3层2011年建暂无数据 - 马銮湾”
            if '层)' in temp:
                sep = '层)'
            else:
                sep = '层'
            after_sep = (temp.split(sep)) if sep in temp else temp
            # 拆分完后再把sep加回来
            if len(after_sep) > 1 and sep in temp:
                after_sep[0] = after_sep[0] + sep

            # 这个是第一行“东方高尔夫别墅 | 6室2厅 | 372.54平米 | 南 | 其他”
            thisdetail = detail.contents[-1].split('|')

            # 把第一行和第二行的数组拼起来
            if isinstance(after_sep, list):
                thisdetail = thisdetail + after_sep
            else:
                thisdetail.append(after_sep)

            for item in thisdetail:
                d1 = self.parse_item(item)
                if len(d1) > 0:
                    if ('advantage' in each_data.keys()) and ('advantage' in d1.keys()):
                        each_data['advantage'] = each_data['advantage'] + ',' + d1['advantage']
                    else:
                        each_data = dict(each_data, **d1)
            each_data['total_price'] = int(round(float(price.get_text()),0))
            each_data['price'] = round(float(each_data['total_price']*10000/each_data['area']),2)
            each_data['from'] = "Beike"

            each_data = self.pipe(each_data)

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)

        return page_datas

if __name__ == "__main__":
    downloader = Downloader.Downloader()
    parser = BeikePage()
    url = ' https://xm.ke.com/ershoufang/pg1rs嘉源新城（53、55、57）'
    html_cont = downloader.download(url)
    soup = parser.get_soup(html_cont)
    urls,datas = parser.page_parse(html_cont)
    # ToolsBox.priList(urls)
    # ToolsBox.priList(urls)
