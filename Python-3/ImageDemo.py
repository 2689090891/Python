'''
    批量下载图片
    采用伪装浏览器的方式爬取豆瓣网站首页图片，保存到指定路径文件夹下
'''

import urllib.request,socket,re,sys,os

#定义文件保存路径
targetPath = "G:\\img"

def saveFile(path):
    #检测当前路径有效性
    if not os.path.isdir(targetPath):
        os.mkdir(targetPath)

    #设置每个图片的路径
    pos = path.rindex('/')
    t = os.path.join(targetPath,path[pos+1:])
    return t

url = "http://www.douban.com/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

req = urllib.request.Request(url = url, headers = headers)

res = urllib.request.urlopen(req)

data = res.read()

for link, t in set(re.findall(r'(https:[^s]*?(jpg|png|gif))',str(data))):
    print(link)
    try:
        urllib.request.urlretrieve(link,saveFile(link))
    except:
        print("失败")