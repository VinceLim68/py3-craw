#coding:utf-8
import traceback  
import datetime

class UrlManager(object):

    def __init__(self) -> object:
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url):
        url = url.strip()
        if url is None or url == "":
            return False
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
            return url
        return False


    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    @property
    def get_new_url(self) -> object:
        try:
            if len(self.new_urls) != 0:
                # n1,o1 = self.get_quantity()
                # print("原来:new({0}),old({1})".format(n1,o1))
                new_url = self.new_urls.pop()
                self.old_urls.add(new_url)
                # n2,o2 = self.get_quantity()
                # print("现在:new({0}),old({1})".format(n2,o2))
                return new_url
            else:
                print('这里没有urls了！')
        except:
            with open('log.txt','a+') as fout:
                fout.write(str(datetime.datetime.now()) + '\n')
                fout.write("this is in url_manage ,the len of the new_urls is %s \n"%len(self.new_urls))
                traceback.print_exc(file=fout) 
                traceback.print_exc()

    def get_quantity(self):
        return len(self.new_urls),len(self.old_urls)
