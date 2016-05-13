#coding=utf-8

import re
import urllib
import HTMLParser

def getHtml(url):
    page=urllib.urlopen(url)
    html=page.read()
    return html

# def getImg(html):
#     reg = r'src="(.+?\.jpg"pic_ext'
#     imgre=re.compile(reg)
#     imglist=re.findall(imgre, html)
#     return imglist

html=getHtml("http://www.baidu.com/s?tn=baiduhome_pg&rsv_idx=2&wd=股票")
print html