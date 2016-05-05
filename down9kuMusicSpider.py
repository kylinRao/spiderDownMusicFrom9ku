#coding=utf-8
import re,os
from selenium import webdriver
import cookielib,urllib2
from BeautifulSoup import BeautifulSoup
from selenium.webdriver.common.keys import Keys  #需要引入keys包
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
import time
import unittest
##import testCases


global loginUrl
loginUrl= r'http://home.9ku.com/do.php?ac=71ee30ae117cddace55bd01714904227'
global path_js
path_js = r"D:\software\work\PhantomJs\PhantomJs\bin\Debug\phantomjs"

global storeDir
storeDir = ur"K:\songFrom9Ku"
def convert2unicode(inputS):
    #input 可以是str，可以是unicode
    if isinstance(inputS,unicode):
        return inputS
    if isinstance(inputS,str):
        return inputS.decode('utf-8')
class downMusic:
    pageNum = 1
    downCount = 0
    global path_js
    global loginUrl
    
    
    def __init__(self,singerName,name,password,MAXDOWN ):
        self.singerName = singerName
        self.name=name
        self.password = password
        self.MAXDOWN = int(MAXDOWN)
        
    def make_cookie(self,domain,name, value):            
        return cookielib.Cookie(
            version=0,
            domain=domain,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain_specified=True,
            domain_initial_dot=False,   
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None
            )
    def login(self):
        #登陆，创造cookie
        print "login"
        driver=webdriver.PhantomJS(path_js)
        driver.get(loginUrl)
        time.sleep(1)
        driver.get_screenshot_as_file(ur'D:/登陆前.png')
        driver.find_element_by_xpath('//*/input[@name="phone"]').send_keys(self.name)
        driver.find_element_by_xpath('//*[@name="password"]').send_keys(self.password)
        driver.find_element_by_xpath('//*[@name="loginsubmit"]').click()
        
##        print(ur'已实现登录')
        ##中文字符的打印输出一定要加u
        driver.get_screenshot_as_file(ur'D:/登陆后.png')
        phCookieList = driver.get_cookies()
        driver.close()#cookie已经得到了，浏览器就关闭掉吧
        return phCookieList
    def phCookie2urlcookie(self,phCookieList):
        ####获取适用于opener.open()的cookie
        print convert2unicode("phCookie2urlcookie is runing \n")
        urlCookie = cookielib.CookieJar()
        print type(phCookieList)
        print phCookieList
        for cookiedir in phCookieList:
            if (cookiedir.has_key('domain')&cookiedir.has_key('name')&cookiedir.has_key('value')):
                urlCookie.set_cookie(self.make_cookie(cookiedir['domain'],cookiedir['name'],cookiedir['value']))
        print urlCookie
        print "this is cookie"
        for i in urlCookie:
            print i
        return urlCookie
    def getMusicNameList(self,tempPage):
        #获取歌手在9ku网的所有歌曲列表
        musicUrlDir={}
        musicNameList = []
        musicid = []

        print "getMusicNameList is running"
        print convert2unicode(self.singerName)
        print type (self.singerName)
        print type ("http://baidu.9ku.com/song/")
        url = "http://baidu.9ku.com/song/{singerName}/{tempPage}".format(singerName = self.singerName,tempPage=tempPage)

        print convert2unicode(url)
        
        html = urllib2.urlopen(url)
        BS = BeautifulSoup(html)
        #获取歌曲页数
        if tempPage == 1:
            if BS.find('a',attrs={'title':u'尾页'}):
                shourtPageUrl = BS.find('a',attrs={'title':u'尾页'})['href']
            else:                
                assert 0,convert2unicode('这个，好像没有作品额，要不重新来下？或者没有页标，奴家搞不定啦。')
        
            pat = re.compile(r'/[0-9]+/')
            self.pageNum = pat.search(shourtPageUrl).group(0).replace('/','')
##        print pageNum,type(pageNum)
        
        
        
        
        SongNameBS = BS.findAll('a',attrs={'class':'songName','target':'_1'})
        for song in SongNameBS:
            if song:
                if (song.string != None)&(song['href'] != None):
                    songName = str(song.string).replace('\\','').replace('/','')        
                    
                    songId = song['href'].replace('http://www.9ku.com/play/','').replace('.htm','')
                    songDownUrl = 'http://home.9ku.com/mp3down.php?id={songId}'.format(songId = songId)
                    musicUrlDir[songName] = songDownUrl

                    
                    

        
        return musicUrlDir
    

    def downAndWritFiles(self,musicUrlDir,urlCookie):
        global storeDir
        global MAXDOWN
        if musicUrlDir=={}:
            print "0 song(s) will be downloaded!"
            return None
        keyNameValueUrl =  musicUrlDir
        keyUrlValueName = {v:k for k,v in keyNameValueUrl.items()}
        for name,url in keyNameValueUrl.items():
            print convert2unicode(url)

            temdir = storeDir +u'\\'+self.singerName.decode('utf-8') +u'\\'
            print convert2unicode(temdir)
            if not os.path.exists(temdir):
                os.makedirs (temdir)
            filename = temdir +u'【{singerName}】'.format(singerName=self.singerName.decode('utf-8'))+keyUrlValueName[url.decode('utf-8')].decode('utf-8')+u'.mp3'
            print u"downloading {filename} using url:{url}\n".format(filename=filename,url=url)
            #下载歌曲
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(urlCookie))
            
            binMusic = opener.open(url).read()
            #保存到本地
            with open(filename,'wb') as f:
                f.write(binMusic)
                self.downCount = self.downCount+1
                print '{downCount} songs have been downloaded'.format(downCount = self.downCount)
                print '------------------------------------------------'
                if self.downCount >= self.MAXDOWN:
                    assert 0,'you download enough'
        return None
    def start(self):
        phCookieList = self.login()
        urlCookie = self.phCookie2urlcookie(phCookieList)
        tempPage = 1
        while(tempPage <= int(self.pageNum)):
            musicUrlDir = self.getMusicNameList(tempPage)
            
            self.downAndWritFiles(musicUrlDir,urlCookie)
            tempPage = tempPage+1

            print convert2unicode('pageNum = {pageNum}'.format(pageNum=self.pageNum))
        print "end download......"
        return musicUrlDir
    
##        
        
        
        


if __name__=="__main__":
##    unittest.main()

##    print u"你要下载那个明星的歌呢？写下他的名字吧："
##    singerName=raw_input()
##    print type(singerName)
##    print u"一首歌曲2,3M的样子，下载多了硬盘受不了，最大下在多少啊，大神！给个数吧："
##    MAXDOWN=raw_input()
    singer = ['刘德华','张学友','周华健','周杰伦','陈奕迅港台女：王菲','邓丽君','高胜美','张惠妹','陈慧琳','筷子兄弟','凤凰传奇','TFBOYS','S.H.E','五月天','汪峰','张杰','张靓颖','本兮',
              '李宇春','','庄心妍','周杰伦','林俊杰','王力宏','汪东城','陈势安','邓紫棋','范玮琪','张惠妹','田馥甄','王菲']
    account = ''#填写电话号码
    password= ''#填写密码
    for name in singer:
        k9 = downMusic(name,account,password,'1000')
        k9.start()
    

        
            
