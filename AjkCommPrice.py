import AjkPage,PageParser,ToolsBox,Downloader
import datetime
import traceback

class AjkCommPrice(AjkPage.AjkPage):
    def parse_datas(self, soup):
        totalfind = soup.select("span.tit em")
        if 0 == ToolsBox.strToInt(totalfind[1].get_text()): return '0'
        page_datas = []
        communitys = soup.select("h3 > a")
        adds = soup.select('.li-info>address')
        dates = soup.select('p.date')
        prices = soup.select('p>strong')
        forsales = soup.select('p.bot-tag>span>a')
        for community, add, date, price,forsale in zip(communitys, adds, dates, prices,forsales):
            each_data = dict()
            each_data['community_name'] = community.get('title')
            each_data['community_url'] = community.get('href')
            add1 = ToolsBox.clearStr(add.get_text())
            addlist = add1.split('］')
            if len(addlist)>1:
                regionlist = addlist[0].replace('［','').split('-')
                if len(regionlist) > 1:
                    each_data['region'], each_data['block'] = regionlist
                else:
                    each_data['region'] = regionlist
                each_data['address'] = addlist[1]
            else:
                each_data['address'] = add1
            each_data['builded_year'] = ToolsBox.strToInt(date.get_text())
            each_data['forsale_num'] = ToolsBox.strToInt(forsale.get_text())
            each_data['price'] = ToolsBox.strToInt(price.get_text())
            # each_data['date']
            each_data['from'] = "AJK"

            if each_data:
                page_datas.append(each_data)
            else:
                if ToolsBox.ShowInvalideData(each_data): page_datas.append(each_data)
            # ToolsBox.printDic(page_datas)
        return page_datas

    # def parse_urls(self, soup):
    #     numbers = soup.select("span.tit")
    #     return ToolsBox.strToInt(numbers[0].get_text())
        # new_urls = set()
        # pages = soup.find('div', class_='multi-page')
        # if pages == None :
        #     print("本页面没有翻页链接。")
        # else:
        #     links = pages.find_all('a')
        #     for url in links:
        #         new_urls.add(url['href'])
        # return new_urls

