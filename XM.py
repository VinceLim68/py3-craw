import MassController,XmhousePage,LejvPage,GanjiPage,MaitianPage
num = 0
url=['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_2.html']
XM = MassController.MassController(XmhousePage.XmhousePage)
XM.total = num
XM.craw_controller(url)
# num += XM.total
num = XM.total + XM.outputer.out_mysql()
print('==================厦门HOUSE网共抓取{0}个记录=================='.format(num))

url = ['http://xm.esf.leju.com/house']
LEJV = MassController.MassController(LejvPage.LejvPage)
LEJV.delay = 3
LEJV.headers = dict(Host="xm.esf.leju.com", Origin="http://xm.esf.leju.com", Referer="http://xm.esf.leju.com/house/")
LEJV.total = num
LEJV.craw_controller(url)
# num += LEJV.total
num = LEJV.total + LEJV.outputer.out_mysql()
print('==================厦门HOUSE网、乐居网共抓取{0}个记录=================='.format(num))

url = ['http://xm.ganji.com/fang5/o2/']
GJ = MassController.MassController(GanjiPage.GanjiPage)
GJ.delay = 3
GJ.headers = dict(Host="xm.ganji.com",  Referer="http://xm.ganji.com/fang5/o2/")
GJ.total = num
GJ.craw_controller(url)
#num += GJ.total
num = GJ.total + GJ.outputer.out_mysql()
print('==================厦门HOUSE网、乐居网、赶集网共抓取{0}个记录=================='.format(num))

url = ['http://xm.maitian.cn/esfall/PG2']
MT = MassController.MassController(MaitianPage.MaitianPage)
MT.headers = dict(Host="xm.maitian.cn")
MT.total = num
MT.craw_controller(url)
# num += MT.total
num = MT.total + MT.outputer.out_mysql()
print('==================厦门HOUSE网、乐居网、赶集网、麦田网共抓取{0}个记录=================='.format(num))

