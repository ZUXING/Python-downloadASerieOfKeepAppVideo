import requests
#网址输入在这里
print("要下载哪个Keep视频>")
#input()用来输入String
r=requests.get(r''+input())
#调整编码，如果不是UTF-8，那有可能是GB2312
r.encoding = 'UTF-8'
# <Response [200]>
#print(r)
# <class 'requests.models.Response'>
#print(type(r))
# 200
#print(r.status_code)
# Page_content
#print(r.text)

#上一步用来获得网页内容，下一步开始分解<a>标签
import re

from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, "html.parser")
#视频计数
video_count = 1
#性别判断
print("需要的视频模特de性别是? f=女 m=男>")
vid_gender = input()
#匹配分割条件
for allVideoContent in soup.find_all('a', href=re.compile('exercises')):
    #所有包含视频的网址都在这里了
    #print(allVideoContent.get('href'))

    

    #此时，需要再次调用爬虫，爬取视频链接
    vid_r=requests.get(r'https://www.keep.com'+allVideoContent.get('href')[:-1]+vid_gender)
    #调整编码，如果不是UTF-8，那有可能是GB2312
    vid_r.encoding = 'UTF-8'

    #每个视频页面的HTML代码可以通过这个print显示
    #print(vid_r.text)
    vid_Soup = BeautifulSoup(vid_r.text, "html.parser")

    #显示文件名和链接
    print("正在下载:"+vid_Soup.title.string[:-5])
    print(vid_Soup.find(attrs={'data-src':re.compile('https')}).get('data-src'))

    #获取文件内容
    vid_f = requests.get(vid_Soup.find(attrs={'data-src':re.compile('https')}).get('data-src'))
    #另存为
    with open(str(video_count)+'_'+vid_Soup.title.string[:-5]+".mp4","wb") as code:
        code.write(vid_f.content)
    #计数器+1
    video_count=video_count+1
