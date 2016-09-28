import urllib
import urllib2
import random
import sqlite3
import re

def pipei(html,r):
    p=re.compile(r,re.S)
    finds = re.findall(p, html)
    return finds

def get_header(pid):
    headers=[
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    ]
    Referer='http://www.luogu.org/problem/lists?name=&orderitem=&order=&tag=&page='+str((pid-1000)/50+1)
    return {'User-Agent':headers[random.randint(0,3)],'Referer':Referer}

def get_html(url,pid):
    req = urllib2.Request(url=url, headers=get_header(pid))
    response = urllib2.urlopen(req)
    return response.read()

def get_real_text(raw_html):
    result = raw_html.replace('<p>','')
    result = result.replace('</p>','\n')
    result = result.replace('<br>','\n')
    result = result.replace('\'',"''")
    result = result.strip()
    return result

def has_value(find):
    if find:
        return get_real_text(find[0])
    else:
        return ''
