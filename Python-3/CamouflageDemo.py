'''

    伪装浏览器

    对于一些需要登录的网站，如果不是从浏览器发出的请求，则得不到响应。
    所以，我们需要将爬虫程序发出的请求伪装成浏览器正规军。
    具体实现：自定义网页请求报头。

    #实例二：依然爬取豆瓣，采用伪装浏览器的方式

'''

import urllib.request

def saveFile(data):
    path = "G:\\doban.txt"
    f = open(path,'wb')
    f.write(data)
    f.close()

url = "https://www.douban.com/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

req = urllib.request.Request(url=url, headers=headers)

res = urllib.request.urlopen(req)

data = res.read()

#将爬取内容保存到文件中
saveFile(data)

data = data.decode('utf-8')

print(data)