# -*- coding: utf-8 -*-
import wx
import down9kuMusicSpider

app = wx.App()
win = wx.Frame(None,title='title',size=(500,200))
bkg = wx.Panel(win)
def generate(event):
    if (not nameSingersContent.GetValue())|(not loginNameContent.GetValue())|(not loginPasswordContent.GetValue()):
        print "nameSingersContent is {nameSingersContent},type is {typeC}".format(
            nameSingersContent = nameSingersContent.GetValue(),typeC=type(nameSingersContent.GetValue()))
        print "loginNameContent is {loginNameContent},type is {typeC}".format(
            loginNameContent = loginNameContent.GetValue(),typeC=type(loginNameContent.GetValue()))
        print "loginPasswordContent is {loginPasswordContent},type is {typeC}".format(
            loginPasswordContent = loginPasswordContent.GetValue(),typeC=type(loginPasswordContent.GetValue()))
        
        
    else:
        print "start to handle strings!"
        print nameSingersContent.GetValue()
        singer = nameSingersContent.GetValue().encode('utf-8').split('|')
        account = loginNameContent.GetValue().encode('utf-8')#填写电话号码
        password= loginPasswordContent.GetValue().encode('utf-8')#填写密码
        print singer,account,password
        print len(singer),type(singer),type(account),type(password)
        for singerName in singer:
            if singerName:
                k9 = down9kuMusicSpider.downMusic(singerName,account,password,'1000')
                k9.start()
        

#界面框架start
nameSingers = wx.StaticText(bkg,label="nameSingers:")
loginName = wx.StaticText(bkg,label="loginName:")
loginPassword = wx.StaticText(bkg,label="loginPassword:")
##loadButton = wx.Button(bkg,label='Open')


generateButton = wx.Button(bkg,label='generate')
generateButton.Bind(wx.EVT_BUTTON,generate)


nameSingersContent = wx.TextCtrl(bkg)
loginNameContent = wx.TextCtrl(bkg)
loginPasswordContent = wx.TextCtrl(bkg)

##contents = wx.TextCtrl(bkg,style=wx.TE_MULTILINE | wx.HSCROLL)

hbox1 = wx.BoxSizer()
hbox1.Add(nameSingers)
hbox1.Add(nameSingersContent,proportion=1,flag=wx.EXPAND)
##hbox1.Add(saveButton,proportion=0,flag=wx.LEFT,border=5)

hbox2= wx.BoxSizer()
hbox2.Add(loginName)
hbox2.Add(loginNameContent,proportion=1,flag=wx.EXPAND)
##hbox2.Add(saveButton,proportion=0,flag=wx.LEFT,border=5)

hbox3= wx.BoxSizer()
hbox3.Add(loginPassword)
hbox3.Add(loginPasswordContent,proportion=1,flag=wx.EXPAND)
##hbox3.Add(saveButton,proportion=0,flag=wx.LEFT,border=5)
hbox4= wx.BoxSizer()
hbox4.Add(generateButton)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox1,proportion=0,flag=wx.EXPAND | wx.ALL,border=5)
vbox.Add(hbox2,proportion=0,flag=wx.EXPAND | wx.ALL,border=5)
vbox.Add(hbox3,proportion=0,flag=wx.EXPAND | wx.ALL,border=5)
vbox.Add(hbox4,proportion=0,flag=wx.EXPAND | wx.ALL,border=5)
##vbox.Add(contents,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT ,border=5)


bkg.SetSizer(vbox)
#界面框架end



win.Show()
app.MainLoop()
