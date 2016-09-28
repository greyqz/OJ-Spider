#-*- coding:utf-8 -*
import time,sys
import urllib
import urllib2
import random
import sqlite3
import re

def get_url(page):
    return "http://daniu.luogu.org/problem/lists?name=&orderitem=&order=&tag=&page="+str(page)


def pipei(html,r):
    p=re.compile(r,re.S)
    finds = re.findall(p, html)
    return finds


def insert_db(conn,pid,title,beijing,miaoshu,ingeshi,outgeshi,inyangli,outyangli,shuoming,put,down,nandu,putuser,year,saixi):
    conn.execute("INSERT INTO LUOGUPROBLEM (PID,TITLE,BEIJING,MIAOSHU,INGESHI,OUTGESHI,INYANGLI,OUTYANGLI,SHUOMING,PUT,DOWN,NANDU,PUTUSER,YEAR,SAIXI) \
      VALUES ("+pid+',\''+title+'\',\''+beijing+'\',\''+miaoshu+'\',\''+ingeshi+'\',\''+outgeshi+'\',\''+inyangli+'\',\''+outyangli+'\',\''+shuoming+'\','+str(put)+','+str(down)+',\''+nandu+'\',\''+putuser+'\',\''+year+'\',\''+saixi+"\')")

def new_db(conn):
    conn.execute('''CREATE TABLE LUOGUPROBLEM
       (PID           TEXT,
       TITLE          TEXT,
       BEIJING        TEXT,
       MIAOSHU        TEXT,
       INGESHI        TEXT,
       OUTGESHI       TEXT,
       INYANGLI       TEXT,
       OUTYANGLI      TEXT,
       SHUOMING       TEXT,
       PUT            INT,
       DOWN           INT,
       NANDU          TEXT,
       PUTUSER        TEXT,
       year           TEXT,
       SAIXI          TEXT);''')

def get_header(pid):
    headers=[
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    ]
    #Referer='http://daniu.luogu.org/problem/lists?name=&orderitem=&order=&tag=&page='+str((pid-1000)/50+1)
    return {'User-Agent':headers[random.randint(0,3)]}#,'Referer':Referer}

def get_html(url,pid):
    req = urllib2.Request(url=url, headers=get_header(pid))
    response = urllib2.urlopen(req)
    return response.read()

def main():
    conn_old   = sqlite3.connect('luogu.db')
    conn_daniu = sqlite3.connect('luogu_daniu.db')
    new_db(conn_daniu)
    pages = range(1,21)
    while pages:
        page = random.choice(pages)
        pages.remove(page)
        url = get_url(page)
        try:
            html = get_html(url,1001)
            #print "get"+str(page)
        except:
            pages.append(page)
            continue
        pidr = r'<i\ class=\"am-icon-minus\"></i></strong></a.+?P([0-9]+)\ .+?<a\ data-pjax\ href=\"/problem/show\?pid='
        pids = pipei(html,pidr)
        for i in pids:
            problem = conn_old.execute('select * from LUOGUPROBLEM where pid='+i)
            for p in problem:
                insert_db(conn_daniu,p[0],p[1].replace('\'',"''"),p[2].replace('\'',"''"),p[3].replace('\'',"''"),p[4].replace('\'',"''"),p[5].replace('\'',"''"),p[6].replace('\'',"''"),p[7].replace('\'',"''"),p[8].replace('\'',"''"),p[9],p[10],p[11],p[12],p[13],p[14])
                print p[0] + 'insert success'
    conn_daniu.commit()
    conn_daniu.close()
    conn_old.close()

if __name__ == '__main__':
    main()

'''
<div class="am-g lg-table-bg0 lg-table-row">
	<div class="am-u-md-10 lg-table-big t"><a href="/record/lists?uid=6775&amp;pid=3357" target="_blank"><strong class=""><i class="am-icon-minus"></i></strong></a>         <span class="am-badge am-badge-warning am-radius"><i class="am-icon-diamond"></i></span>         P3357        <a data-pjax="" href="/problem/show?pid=3357">最长 k可重线段集问题</a>
        <span class="lg-right am-text-right">
        <span class="am-badge am-radius lg-bg-gray">尚无评定</span><div class="am-text-right"></div>	</span></div>
	<div class="am-u-md-2 lg-table-small">
		<!--0分<br>-->
		<div class="am-progress"><div class="am-progress-bar am-progress-bar-secondary" style="width: 0%">0/0		</div></div>
	</div>
    </div>
'''
