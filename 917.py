import MassController,Page917,ToolsBox
from urllib import parse

class JYQ(MassController.MassController):
    def __init__(self, parseClass):
        super(JYQ, self).__init__(parseClass)
        self.comm_count = 1                         #计数：抓取小区的数量
        self.delay = 0
        self.headers = {
            "Referrer Policy": "no - referrer - when - downgrade",
            # "Host": "www.917.com",
        }

    def CommsController(self,url):
        self.craw_controller(url)
        while self.comms.has_new_url():
            comm = self.comms.get_new_url
            comm = ToolsBox.clear_comm(comm)
            c1,c2 = self.comms.get_quantity()
            comm_url = "https://xm.917.com/sell/?k=" + parse.quote(comm)
            print('*******{0}/{1}:{2}*********'.format(self.comm_count,c1+c2,comm))
            url_list = []
            url_list.append(comm_url)
            self.craw_controller(url_list)
            self.comm_count += 1

        self.total = self.total + self.outputer.out_mysql()
        print('==================共抓取{0}个记录=================='.format(self.total))

if __name__=="__main__":
    url = ["https://xm.917.com/sell/pn2/"]
    # comm = '龙华大厦(南湖花园）'
    # comm_url = "https://www.917.com/sell/?k=" + parse.quote(comm)
    # print(comm_url)
    jyq = JYQ(Page917.www917Page)
    jyq.CommsController(url)
