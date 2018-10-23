import MassController,XmhousePage,LejvPage,GanjiPage,MaitianPage
num = 0
url=['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_2.html']
XM = MassController.MassController(XmhousePage.XmhousePage)
# XM.total = num
XM.craw_controller(url)
# num += XM.total
XM.total = XM.total + XM.outputer.out_mysql()
num = XM.total
print('厦门HOUSE:{0},共{1}个'.format(XM.total,num))

url = ['http://xm.esf.leju.com/house']
LEJV = MassController.MassController(LejvPage.LejvPage)
LEJV.delay = 3
LEJV.headers = dict(Host="xm.esf.leju.com", Origin="http://xm.esf.leju.com", Referer="http://xm.esf.leju.com/house/")
# LEJV.total = num
LEJV.craw_controller(url)
LEJV.total = LEJV.total + LEJV.outputer.out_mysql()
num += LEJV.total
print('厦门HOUSE网:{0},乐居网{1}个,共{2}个'.format(XM.total,LEJV.total,num))

url = ['http://xm.ganji.com/fang5/o2/']
GJ = MassController.MassController(GanjiPage.GanjiPage)
GJ.delay = 3
GJ.headers = dict(Host="xm.ganji.com",Referer="http://xm.ganji.com/fang5/o2/")
# GJ.total = num
GJ.craw_controller(url)
GJ.total = GJ.total + GJ.outputer.out_mysql()
num += GJ.total
print('厦门HOUSE网:{0},乐居网{1},赶集网{2},共{3}个'.format(XM.total, LEJV.total, GJ.total,num))

url = ['http://xm.maitian.cn/esfall/PG2']
MT = MassController.MassController(MaitianPage.MaitianPage)
MT.delay = 3
MT.headers = {'Host': "xm.maitian.cn", 'Referer': "http://xm.maitian.cn/esfall/PG2"}
# MT.total = num
MT.craw_controller(url)
MT.total = MT.total + MT.outputer.out_mysql()
print(MT.total)
num += MT.total
print('厦门HOUSE网:{0},乐居网{1},赶集网{2},麦田:{3},共{4}个'.format(XM.total,LEJV.total,GJ.total,MT.total,num))


