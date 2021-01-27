import MassController,SfPage,ToolsBox
# from urllib import parse

class SF(MassController.MassController):
    def __init__(self, parseClass):
        super(SF, self).__init__(parseClass)
        self.comm_count = 1                         #计数：抓取小区的数量
        self.headers = {
            # "Host":"esf.xm.fang.com",
            # "Host":"xm.esf.fang.com",
            # "Origin":"http://esf.xm.fang.com",
            # "Referer":"https://xm.esf.fang.com/",
            # "upgrade-insecure-requests": "1",
            # "accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
            # "accept-encoding": "gzip, deflate, br",
            # "accept-language": "zh-CN, zh; q = 0.9",
            # "cache - control": "max - age = 0",
            "Request Method": "GET",
            "Status Code": "200",
            "Remote Address": "124.251.86.61: 443",
            "Referrer Policy": "no-referrer-when-downgrade",
            "accept": "text/html, application/xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN, zh; q = 0.9",
            "cache-control": "max-age = 0",
            "sec-fetch-mode": "nested-navigate",
            "sec-fetch-site": "same-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            # "cookie": "global_cookie=a7gnft7o62ylzcmb255fb09dw18kegkso4s; newhouse_user_guid=C69DEA2D-6140-D81D-292B-C8D42AA871C5; city=xm; __utma=147393320.1300113496.1598760635.1604542600.1605496393.8; __utmz=147393320.1605496393.8.7.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-a64299b1c8a129806f/; g_sourcepage=esf_fy%5Elb_pc; __utmc=147393320; __utmb=147393320.42.10.1605496393; unique_cookie=U_v6itq2xzb7l2f8wzrsn3p2mif13khjzri6w*7",
            "referer": "https: // xm.esf.fang.com /",
            # ":authority": "xm.esf.fang.com"
        }
        self.delay = 1

    def add_comm(self,data):
        #把添加小区列表提出来，因为会有不一样的需求，有的需要小区名称，有的需要小区链接
        comm_add = data['community_name']
        comm = self.comms.add_new_url(data['comm_url'])
        if comm:
            print('>>>>>>>>>>>>>>>>{0}:{1}'.format(comm_add, comm))

        # if len(comm_add) > 15:
        #     print('{0}---->名字过长的小区名将被忽略。'.format(comm_add))
        # else:
        #     comm = self.comms.add_new_url(data['comm_url'])
        #     if comm:
        #         print('>>>>>>>>>>>>>>>>{0}:{1}'.format(comm_add,comm))

    def CommsController(self,url):
        # print(self.headers)
        self.craw_controller(url)
        while self.comms.has_new_url():
            comm = self.comms.get_new_url
            c1,c2 = self.comms.get_quantity()
            comm_url = 'https://xm.esf.fang.com/' + comm
            # comm_url = 'http://xm.esf.fang.com/house/c61-kw' + comm + '/'
            print('*******{0}/{1}:{2}*********'.format(self.comm_count,c1+c2,comm))
            url_list = []
            url_list.append(comm_url)
            self.craw_controller(url_list)
            self.comm_count += 1

        self.total = self.total + self.outputer.out_mysql()
        print('==================共抓取{0}个记录=================='.format(self.total))

if __name__=="__main__":
    # url = ["https://esf.xm.fang.com/"]
    url = ["https://xm.esf.fang.com/"]
    SFmain = SF(SfPage.SfPage)
    SFmain.CommsController(url)
