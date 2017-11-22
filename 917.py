import MassController,Page917

class JYQ(MassController.MassController):
    def __init__(self, parseClass):
        super(JYQ, self).__init__(parseClass)
        self.comm_count = 1                         #计数：抓取小区的数量
        self.delay = 0
        self.headers = {
            "Host": "www.917.com",
            "Referer": "http://www.917.com/",
        }

    def CommsController(self,url):
        self.craw_controller(url)
        while self.comms.has_new_url():
            comm = self.comms.get_new_url()
            c1,c2 = self.comms.get_quantity()
            comm_url = "http://www.917.com/sell/?k=" + comm
            print('*******{0}/{1}:{2}*********'.format(self.comm_count,c1+c2,comm))
            url_list = []
            url_list.append(comm_url)
            self.craw_controller(url_list)
            self.comm_count += 1

        self.total = self.total + self.outputer.out_mysql()

if __name__=="__main__":
    url = ["http://www.917.com/sell/pn2/"]
    jyq = JYQ(Page917.www917Page)
    jyq.CommsController(url)
