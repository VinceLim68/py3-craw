import MassController,XmhousePage,LejvPage,GanjiPage,MaitianPage,DanxiaPage
num = 0
url=['http://esf.xmhouse.com/sell/t4_r_a_u_l_z_s_itp_b_it_if_ih_p-_ar-_pt_o_ps_2.html']
XM = MassController.MassController(XmhousePage.XmhousePage)
XM.craw_controller(url)
XM.total = XM.total + XM.outputer.out_mysql()
num = XM.total
print('厦门HOUSE:{0},共{1}个'.format(XM.total,num))

url = ['http://xm.esf.leju.com/house']
LEJV = MassController.MassController(LejvPage.LejvPage)
LEJV.delay = 3
LEJV.headers = dict(Host="xm.esf.leju.com", Origin="http://xm.esf.leju.com", Referer="http://xm.esf.leju.com/house/")
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

url = ['https://danxia.com/house/all/PG2']
DX = MassController.MassController(DanxiaPage.DanxiaPage)
DX.delay = 0
DX.headers = {
        "Referer": "https://danxia.com/house/all",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
DX.craw_controller(url)
DX.total = DX.total + DX.outputer.out_mysql()
num += DX.total
print('厦门HOUSE网:{0},乐居网{1},赶集网{2},丹夏网{3},共{4}个'.format(XM.total, LEJV.total, GJ.total,DX.total,num))

url = ['http://xm.maitian.cn/esfall/PG2']
MT = MassController.MassController(MaitianPage.MaitianPage)
MT.delay = 8
MT.headers = {'Host': "xm.maitian.cn", 'Referer': "http://xm.maitian.cn/esfall/PG2"}
MT.craw_controller(url)
MT.total = MT.total + MT.outputer.out_mysql()
num += MT.total
print('厦门HOUSE网:{0},乐居网{1},赶集网{2},丹夏网{3},麦田:{4},共{5}个'.format(XM.total, LEJV.total, GJ.total,DX.total,MT.total,num))


