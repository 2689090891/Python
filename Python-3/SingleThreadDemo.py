'''
    单线程爬取CSDN博文内容
    爬取内容包括：
        1.发表日期
        2.是否原创标记
        3.博文标题
        4.博文链接
        5.浏览量
        6.评论量
'''

import urllib.request,re,time,random,gzip,os

#定义保存文件函数
def saveFile(data,i):
    path = "G:\\Spider"
    if not os.path.isdir(path):
        os.mkdir(path)
    pathTxt = "G:\\Spider\\第"+str(i+1)+"页.txt"
    file = open(pathTxt,'wb')
    # windows的换行是\r\n，unix的是\n，mac的是\r
    page = '当前页：'+str(i+1)+'\r\n\r\n'
    file.write(page.encode('gbk','ignore'))
    #将博文信息写入到文件(以utf-8保存文件声明为gbk)
    for d in data:
        d = str(d) + '\r\n'
        #在对unicode字符编码时，添加ignore参数，忽略无法无法编码的字符
        file.write(d.encode('gbk','ignore'))
    file.close()

#解压缩数据
def ungzip(data):
    try:
        print('正在解压缩...')
        data = gzip.decompress(data)
        print('解压缩完毕...')
    except:
        print('未经压缩，无需解压...')
    return data

#爬虫类
class Spider:
    def __init__(self,pageIdx=1,url='http://blog.csdn.net/fly_yr/article/list/1'):
        #默认当前页
        self.pageIdx = pageIdx
        self.url = url[0:url.rfind('/')+1] + str(pageIdx)
        self.headers = {
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh - CN, zh;q = 0.8',
            'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / '
                          '537.36(KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36',
            'Connection': 'keep - alive',
            'Host': 'blog.csdn.net'
        }

    #求总页数
    def getPages(self):
        req = urllib.request.Request(url = self.url,headers=self.headers)
        res = urllib.request.urlopen(req)

        #从主页抓取的内容是压缩后的内容，先解压缩
        data = res.read()
        data = ungzip(data)
        data = data.decode('utf-8')

        pages = r'<div.*?pagelist">.*?<span>.*?共(.*?)页</span>'
        #计算总页数
        pattern = re.compile(pages, re.DOTALL)
        pagesNum = re.findall(pattern,data)[0]
        return pagesNum

    #设置要抓取的页面
    def setPage(self,idx):
        self.url = self.url[0:self.url.rfind('/') + 1] + str(idx)

    #读取博文信息
    def readData(self):
        ret = []
        str = r'<div.*?list_item article_item">.*?article_title">.*?ico ico_type_(.*?)">' \
              r'</span>.*?link_title"><a href="(.*?)">(.*?)</a>.*?article_description">(.*?)' \
              r'</div>.*?article_manage">.*?link_postdate">(.*?)-(.*?)-(.*?) (.*?)</span>.*?l' \
              r'ink_view".*?阅读次数">阅读</a>(.*?)</span>.*?"link_comments".*?"评论次数".*?评论</a>(.*?)</span>'

        req = urllib.request.Request(url=self.url,headers=self.headers)
        res = urllib.request.urlopen(req)

        #从主页抓取内容的是解压缩后的内容，先解压缩
        data = res.read()
        data = ungzip(data)
        data = data.decode('utf-8')
        pattern = re.compile(str,re.DOTALL)
        items = re.findall(pattern,data)
        for item in items:
            if(item[0] == 'Original'):
                stri = '原'
            else:
                stri = '转'
            #str.strip().replace('\n','')去空格和换行符，优化格式
            ret.append('◇ '+item[4]+'年'+item[5]+'月'+item[6]+'日'+'  时间：'+item[7]+'\t'+stri+'\r\n标题：'
                       +item[2].strip()+'\r\n简介：'+item[3].strip().replace('\n','')+'\r\n'+'连接：http://blog.csdn.net'
                       +item[1]+'\r\n'+'阅读'+item[8]+'\t评论：'+item[9]+'\r\n')
        return ret

#定义爬虫对象
cs = Spider()

#求取
pagesNum = int(cs.getPages())
print("博文总页数：",pagesNum)

for idx in range(pagesNum):
    cs.setPage(idx)
    print('当前页：',idx + 1)

    #读取当前页的所有博文,结果为list类型
    papers = cs.readData()
    saveFile(papers,idx)