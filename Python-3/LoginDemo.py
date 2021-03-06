'''
    模拟登录抓取网页信息

'''

import gzip
import http.cookiejar
import urllib.parse
import urllib.request
import re


#解压缩函数
def ungzip(data):
    try:
        print("正在解压缩...")
        data = gzip.decompress(data)
        print("解压完毕...")
    except:
        print("未经压缩，无需解压...")
    return data

#构造文件头
def getOpener(header):
    #设置一个cookie处理器,他负责从服务器下载cookie到本地,并且在发送请求时带上本地的cookie
    cookieJar = http.cookiejar.CookieJar()
    cp = urllib.request.HTTPCookieProcessor(cookieJar)
    opener = urllib.request.build_opener(cp)
    headers = []
    for key,value in header.items():
        elem = (key,value)
        headers.append(elem)
    opener.addheaders = headers
    return opener

#获取_xsrf
def getXsrf1(data):
    cer = re.compile('name=\"_xsrf\" value=\"(.*)\"',flags=0)
    strlist = cer.findall(data)
    return strlist[0]

#根据网站报头信息设置headers
headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) ' \
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Host': 'www.zhihu.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'DNT':'1'
}

url = "https://www.zhihu.com/"
req = urllib.request.Request(url,headers = headers)
res = urllib.request.urlopen(req)

#读取知乎首页内容，获得'_xsrf'
data = res.read()
data = ungzip(data)
_xsrf = getXsrf1(data.decode('utf-8'))

opener = getOpener(headers)

#post数据接收和处理的页面(我们要向这个页面发送我们构造的Post数据)
url += 'login/phone_num'
name = '15097793990'
password = '12345678'

#分析构造post数据
postDict = {
    '_xsrf':_xsrf,
    'phone':name,
    'password':password,
    'remember_me':'true'
}

#给post数据编码
postData = urllib.parse.urlencode(postDict).encode()

#构造请求
res = opener.open(url,postData)
data = res.read()

#解压缩
data = ungzip(data)
print(data.decode())