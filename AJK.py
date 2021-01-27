import MassController,AjkPage,ToolsBox
from urllib import parse

class AJK(MassController.MassController):
    def __init__(self, parseClass):
        super(AJK, self).__init__(parseClass)       #AJK继承Mass,这句是在Mass中传入对象
        self.comm_count = 1                         #计数：抓取小区的数量
        self.delay = 5
        self.headers = {
            "Request Method": "GET",
            "Status Code": "200",
            "Remote Address": "123.206.235.145: 443",
            "Referrer Policy": "no - referrer - when - downgrade",
            # "Host": "xm.anjuke.com",
            # "Referer": "http://xm.anjuke.com/",
        }

    def CommsController(self,url):
        self.craw_controller(url)
        while self.comms.has_new_url():
            comm = self.comms.get_new_url
            comm = ToolsBox.clear_comm(comm)
            c1,c2 = self.comms.get_quantity()
            comm_url = 'https://xm.anjuke.com/sale/p1-rd1/?kw=' + parse.quote(comm) + '&from_url=kw_final#filtersort'
            print('*******{0}/{1}:{2}*********'.format(self.comm_count,c1+c2,comm))
            url_list = []
            url_list.append(comm_url)
            self.craw_controller(url_list)
            self.comm_count += 1

        self.total = self.total + self.outputer.out_mysql()
        print('==================共抓取{0}个记录=================='.format(self.total))

if __name__=="__main__":
    url = ["https://xm.anjuke.com/sale/p2/?from=esf_list"]
    ajk = AJK(AjkPage.AjkPage)
    ajk.CommsController(url)
