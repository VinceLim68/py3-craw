import MassController,SfPage,ToolsBox
# from urllib import parse

class SF(MassController.MassController):
    def __init__(self, parseClass):
        super(SF, self).__init__(parseClass)
        self.comm_count = 1                         #计数：抓取小区的数量
        self.headers = {
            # "Host":"esf.xm.fang.com",
            "Host":"xm.esf.fang.com",
            # "Origin":"http://esf.xm.fang.com",
            "Referer":"http://esf.xm.fang.com/"
        }
        self.delay = 3

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
            comm_url = 'http://esf.xm.fang.com' + comm
            # comm_url = 'http://xm.esf.fang.com/house/c61-kw' + comm + '/'
            print('*******{0}/{1}:{2}*********'.format(self.comm_count,c1+c2,comm))
            url_list = []
            url_list.append(comm_url)
            self.craw_controller(url_list)
            self.comm_count += 1

        self.total = self.total + self.outputer.out_mysql()
        print('==================共抓取{0}个记录=================='.format(self.total))

if __name__=="__main__":
    url = ["http://esf.xm.fang.com/"]
    ajk = SF(SfPage.SfPage)
    ajk.CommsController(url)
