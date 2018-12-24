import MassController,GanjiPage
from urllib import parse

class GJ(MassController.MassController):
    def __init__(self, parseClass):
        super(GJ, self).__init__(parseClass)
        self.comm_count = 1                         #计数：抓取小区的数量
        self.delay = 1
        self.headers = {'Host': "xm.ganji.com", 'Referer': "http://xm.ganji.com/"}

    def CommsController(self,url):
        self.craw_controller(url)
        while self.comms.has_new_url():
            comm = self.comms.get_new_url()
            c1,c2 = self.comms.get_quantity()
            comm_url = "http://xm.ganji.com/wblist/ershoufang/?key=" + parse.quote(comm)
            print('*******{0}/{1}:{2}*********'.format(self.comm_count,c1+c2,comm))
            url_list = []
            url_list.append(comm_url)
            self.craw_controller(url_list)
            self.comm_count += 1

        self.total = self.total + self.outputer.out_mysql()
        print('==================共抓取{0}个记录=================='.format(self.total))

if __name__=="__main__":
    url = ['http://xm.ganji.com/wblist/ershoufang/pn2/']
    gj = GJ(GanjiPage.GanjiPage)
    gj.CommsController(url)