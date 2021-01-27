import MassController,WbPage,ToolsBox
from urllib.parse import quote

class WB(MassController.MassController):
    def __init__(self, parseClass):
        super(WB, self).__init__(parseClass)
        self.comm_count = 1                         #计数：抓取小区的数量
        self.delay = 1
        self.headers = {
            "Request Method": "GET",
            "Status Code": "200 OK",
            "Remote Address": "180.101.49.206:443",
            "Referrer Policy": "no-referrer-when-downgrade"
            # "Host": "xm.58.com",
        }

    def CommsController(self,url):
        self.craw_controller(url)

        while self.comms.has_new_url():
            comm = self.comms.get_new_url
            comm = ToolsBox.clear_comm(comm)
            c1, c2 = self.comms.get_quantity()
            # comm_url = "http://xm.58.com/ershoufang/?key=" + (comm)
            comm_url = "https://xm.58.com/ershoufang/?key=" + quote(comm, safe='/:?=')
            print('*******{0}/{1}:{2}*********'.format(self.comm_count, c1+c2, comm))
            url_list = []
            url_list.append(comm_url)
            self.craw_controller(url_list)
            self.comm_count += 1

        self.total = self.total + self.outputer.out_mysql()
        print('==================共抓取{0}个记录=================='.format(self.total))

if __name__=="__main__":
    url = ['http://xm.58.com/ershoufang/pn2/']
    wb = WB(WbPage.WbPage)
    wb.CommsController(url)
