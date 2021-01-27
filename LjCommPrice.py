import LjPage,ToolsBox

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
