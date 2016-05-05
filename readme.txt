txt文件使用utf-8编码
-----【version1.1】
【特性】
1.抓取大把大把的http://www.9ku.com的歌曲，当然了，如果你要下载单独一首歌曲的话，手动曲下载就好了，也可以考虑后续添加单独下载一首歌曲的特性
2.9ku上全是mp3的歌曲额。。。
3.部分代码，可以实现携带cookie登陆哦
4.使用了phantomjs来登陆和获取cookie
5.掌握了cookie，那就可以用urllib2神奇来搞罗。。
6.增加了个wxpython写的页面额
【使用说明】
1.你要有一个http://www.9ku.com网站的账号才可以
2.多个歌手名字请使用|分割，否则，软件会罢工的哦
3.存储路径，我设置在K盘，你们要自己曲代码里面改哦：
在这个文件里面down9kuMusicSpider.py修改那个路径就好了
	global storeDir
	global storeDir
	storeDir = ur"K:\songFrom9Ku"
【存在的问题】
1.phantomjs执行的时候，有个黑色的页面代码里面driver.close()和driver.quit()都关闭不了，悲剧
【so】
发布罗。。。
