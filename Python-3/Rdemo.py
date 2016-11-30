import urllib.request

url = "http://www.douban.com/"

request = urllib.request.Request(url)

response = urllib.request.urlopen(request)

data = response.read()

data = data.decode('utf-8')

print(data)

#打印爬取网页的各类信息
print("----------------------------")
print(type(response))
print("----------------------------")
print(response.geturl())
print("----------------------------")
print(response.info())
print("----------------------------")
print(response.getcode())