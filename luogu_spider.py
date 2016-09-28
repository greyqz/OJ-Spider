#-*- coding:utf-8 -*
import time,sys
from base import *

def get_url(pid):
    return "http://www.luogu.org/problem/show?pid="+str(pid)#+"&_pjax=.lg-content"

def insert_db(conn,pid,title,beijing,miaoshu,ingeshi,outgeshi,inyangli,outyangli,shuoming,put,down,nandu,putuser,year,saixi):
    conn.execute("INSERT INTO LUOGUPROBLEM (PID,TITLE,BEIJING,MIAOSHU,INGESHI,OUTGESHI,INYANGLI,OUTYANGLI,SHUOMING,PUT,DOWN,NANDU,PUTUSER,YEAR,SAIXI) \
      VALUES ("+str(pid)+',\''+title+'\',\''+beijing+'\',\''+miaoshu+'\',\''+ingeshi+'\',\''+outgeshi+'\',\''+inyangli+'\',\''+outyangli+'\',\''+shuoming+'\','+str(put)+','+str(down)+',\''+nandu+'\',\''+putuser+'\',\''+year+'\',\''+saixi+"\')")

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

def main():
    conn = sqlite3.connect('luogu.db')
    #conn = con.cursor()
    f = open(str(time.time())+'.log','wb')
    new_db(conn)
    pidlist = range(1001,3398)
    chusai = [1366,1448,1543,1544,1545,1612,1639,1668,1669,1670,1671,1672,1673,1674,1675,1676,1677,1693,1694,1695,1696,1697,1698,1699,1700,1701,1711,1749,1753,1787,1788,2204,2211,2621,2641]
    for i in chusai:
        pidlist.remove(i)
    x = 0
    num = len(pidlist)
    while pidlist:
        pid = random.choice(pidlist)
        pidlist.remove(pid)
        #pid = 2983
        url = get_url(pid)
        #print url
        try:
            html = get_html(url,pid)
            x+=1
        except:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'  '+str(x)+'/'+str(num)+'   '+str(pid)+'  failed'
            pidlist.append(pid)
            continue
        titler   = r'<div\ class=\"lg\-toolbar\"\ data\-am\-sticky.+?</strong></a> P.+?\ (.+?)</h1.+?/div>'
        beijingr = r'<h2>题目背景</h2>(.+?)<h2>题目描述</h2>'
        miaoshur = r'<h2>题目描述</h2>(.+?)<h2>输入输出格式</h2>'
        ingeshir = r'<strong>输入格式：</strong>(.+?)<strong>输出格式：</strong>'
        outgeshir= r'<strong>输出格式：</strong>(.+?)<h2>输入输出样例</h2>'
        inyanglir = r'<strong>输入样例#1：</strong>.+?<pre>(.+?)</pre.+?</div>'
        outyanglir= r'<strong>输出样例#1：</strong>.+?<pre>(.+?)</pre.+?</div>'
        shuomingr= r'<h2>说明</h2>(.+?)</div>'
        downr = r'<li><span\ class=\"lg-bignum-num\">(.+?)</span><span\ class=\"lg-bignum-text\">通过</span></li>'
        putr  = r'<span class="lg-bignum-text">通过</span></li><li><span\ class=\"lg-bignum-num\">(.+?)</span><span\ class=\"lg-bignum-text\">提交</span></li>'
        nandur = r'<li><strong>难度</strong.+?span class=\"lg-right\"><span class=.+?>(.+?)</span>'
        putuserr = r'<li><strong>题目提供者</strong><span\ class=\"lg-right\">(.+?)</span></li>'
        tagsr = r'<li><strong>标签</strong>(.+?)</li>'
        yearr  = r'<span\ class=\"am-badge\ am-radius\ lg-bg-green\ \">([0-9]+)</span>'
        tagr  = r'<span\ class=\"am-badge\ am-radius\ lg-bg-pink\ am-hide\">(.+?)</span>'
        saixir = r'<span class="am-badge am-radius lg-bg-bluelight ">(.+?)</span>'
        raw_title = pipei(html,titler)
        if raw_title:
            title = get_real_text(raw_title[0])
            #print title
        else:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'  '+str(x)+'/'+str(num)+'   '+str(pid)+'  pass'
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'  '+str(x)+'/'+str(num)+'   '+str(pid)+'  pass\n')
            continue
        beijing = has_value(pipei(html,beijingr))
        miaoshu = get_real_text(pipei(html,miaoshur)[0])
        ingeshi = get_real_text(pipei(html,ingeshir)[0])
        outgeshi= get_real_text(pipei(html,outgeshir)[0])
        inyangli= has_value(pipei(html,inyanglir))
        outyangli=has_value(pipei(html,outyanglir))
        shuoming= has_value(pipei(html,shuomingr))
        raw_down = pipei(html,downr)
        if raw_down[0].find('<small>K</small>') != -1:
            #down = int(float(raw_down[0])*1000)
            r = r'(.+?)<small>K</small>'
            down = int(float(pipei(raw_down[0],r)[0])*1000)
        else:
            down = int(raw_down[0])
        raw_put = pipei(html,putr)
        if raw_put[0].find('<small>K</small>') != -1:
            #put = int(float(raw_put[0])*1000)
            r = r'(.+?)<small>K</small>'
            put = int(float(pipei(raw_put[0],r)[0])*1000)
        else:
            put = int(raw_put[0])
        nandu = get_real_text(pipei(html,nandur)[0])
        raw_putuser = pipei(html,putuserr)[0]
        if raw_putuser.find('<a') != -1:
            r = r'<a.+?>(.+?)</a>'
            putuser = pipei(raw_putuser,r)[0]
        else:
            putuser = raw_putuser
        raw_tags = pipei(html,tagsr)[0]
        year = has_value(pipei(html,yearr))
        tags = pipei(raw_tags, tagr)
        saixi = has_value(pipei(raw_tags, saixir))
        try:
            insert_db(conn,pid,title,beijing,miaoshu,ingeshi,outgeshi,inyangli,outyangli,shuoming,put,down,nandu,putuser,year,saixi)
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'  '+str(x)+'/'+str(num)+'  '+str(pid)+'  done'
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'  '+str(x)+'/'+str(num)+'  '+str(pid)+'  done\n')
            tagf = open('problem/luogu/'+str(pid)+'.txt','wb')
            for i in tags:
                tagf.write(i+'\n')
            tagf.close()
            time.sleep(random.randint(0,10))
        except:
            conn.commit()
            conn.close()
            f.close()
            sys.exit(0)
        #f = open('problem/luogu/'+str(pid)+'.txt')
    f.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
