import re
import time
import datetime
from time import sleep
import random
import os
import requests
import hashlib
import pymongo
import json
import pymysql

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime as d

requests.packages.urllib3.disable_warnings()
myclient=pymongo.MongoClient("mongodb://89.36.16.54:27017")
database={'host':'89.36.16.54','port':3306,'user':'openbaseuser','password':'@123','db':'openbase','charset':'utf8'}
refresh_time = 3  # 5分钟没有反应，就刷新页面
global_run = d.now()
#判断是否为工作时间
def work_time():
    workTime=['7:00:00','18:30:00']
    dayofweek=datetime.datetime.now().weekday()
    beginwork=datetime.datetime.now().strftime("%Y-%m-%d")+' '+workTime[0]
    endwork=datetime.datetime.now().strftime("%Y-%m-%d")+' '+workTime[1]
    beginworksenconds=time.time()-time.mktime(time.strptime(beginwork,'%Y-%m-%d %H:%M:%S'))
    endworksenconds=time.time()-time.mktime(time.strptime(endwork,'%Y-%m-%d %H:%M:%S'))
    if (int(dayofweek) in range(6)) and int(beginworksenconds)>0 and int (endworksenconds)<0:
        return True
    else:
        return False

#自动化运维脚本——PGY 2019.10.10
def sql_select(app_name='360',enum=True):
    global database
    res=[]
    conn=pymysql.connect(**database)
    cursor=conn.cursor()
    if enum:
        # sql="""select * from spider where status=0 and appname='%s'"""%(app_name)
        sql="""select * from spider where appname='%s'"""%(app_name)
    else:
        sql="""select * from enum where enum_class='swjgip'"""
    cursor.execute(sql)
    res=cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return res
def sql_into_mongo(dbname,tablename,jsondata):
    global myclient
    try:
        mydb=myclient[dbname]
        collist=mydb.list_collection_names()
        if tablename in collist:
            try:
                mydb[tablename].drop()
                mycol=mydb[tablename]
                mycol.insert_many(jsondata)
            except:
                mycol.insert_one(jsondata)
        # x=mydb[tablename].insert_many(jsondata)
        # print(x.inserted_id)
        else:
            try:
                mycol=mydb[tablename]
                mycol.insert_many(jsondata)
            except:
                mycol.insert_one(jsondata)
        myclient.close()
    except:
        pass
def encodemd5(s):
    newmd5=hashlib.md5()
    newmd5.update(s.encode("utf-8"))
    return newmd5.hexdigest()
#文件读取模块
def readfile(cfilename):
    with open(cfilename,'r',encoding='utf-8') as cf:
        lines=cf.readlines()
    return lines   
def login(url,urldt):
    bs = webdriver.Chrome()
    bs.get(url) #地址跳转
    # WebDriverWait(bs,10,0.5).until(lambda bs:bs.find_element_by_id('username'))
    # bs.find_element_by_id('username').send_keys(user)
    # bs.find_element_by_id('userpass').send_keys(passwd)
    # bs.find_element_by_id('login').click()
    time.sleep(1) 
    cookies=bs.get_cookies()
    cookiestr=';'.join(item for item in [item['name']+"="+item["value"] for item in cookies])
    headers_cookie={
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)",
        "Cookie":cookiestr
    }
    bs.get(urldt)
    html=bs.page_source
    # html=get_status(urldt,headers_cookie)
    time.sleep(0.1)
    re_table=re.compile('<br>\\n(.*?)=<input',re.S)  #取公式
    res_table=re.findall(re_table,html)
    resstr=res_table[0]
    resstr=resstr.strip() # 去空白
    da=eval(resstr) #字符串转数学公式
    print(resstr)
    strda=int(da)
    print(strda)
    bs.find_element_by_name('v').send_keys(strda) #
    bs.find_element_by_xpath("//*[@type='submit']").click() #提交
    time.sleep(10)
#无界面request登录方式
def login_req(user,passwd):
    key_360='360EntWebAdminMD5Secret'
    passwd_md5=md5(passwd)
    passwd_token=md5(passwd+key_360)
    url="http://153.12.104.152:8080/login/login"
    headers_cookie={
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)"
    }
    udata={
        'username': user,
        'userpass': passwd_md5,
        'pass_token': passwd_token,
        'keepalive': 'false',
        'length': 15,
        'variety': 2,
        'YII_CSRF_TOKEN': '904c29f0af53621f9afa63bf30a863da7f4f8cbc'
    }
    s=requests.Session()
    res=s.post(url=url,headers=headers_cookie,data=udata,timeout=5)
    net=sql_select('360')
    ctime=datetime.datetime.now()
    nt=datetime.timedelta(days=-10)
    etime=ctime+nt
    strctime=ctime.strftime("%Y-%m-%d")
    stretime=etime.strftime("%Y-%m-%d")
    for i in net:        
        mongo_table=i[0]
        bool_list=i[5]
        url=i[4]
        url=url.replace('[ctime]',strctime)
        url=url.replace('[etime]',stretime)      
        strstatus=get_status_res(url,s)
        strstatus=strstatus.replace("/","")
        strstatus=strstatus.replace("\\","")
        strstatus=strstatus.replace("\\\\","")
        resdict=json.loads(strstatus,strict=False)
        if bool_list=='1':
            sql_into_mongo('netMonitor',mongo_table,resdict['data']['list'])
        elif bool_list=='0':
            sql_into_mongo('netMonitor',mongo_table,resdict['data'])
    s.close()
        # print(strstatus)
def get_status(url,headers_cookie):
    res=requests.get(url,headers=headers_cookie)
    strstatus=''
    if res.status_code==200:
        strstatus=res.text.encode().decode('unicode_escape')#网页编码中文转换    
    return strstatus
#无界面方法
def get_status_res(url,s):
    res=s.get(url)
    strstatus=''
    if res.status_code==200:
        strstatus=res.text.encode().decode('unicode_escape')#网页编码中文转换    
    return strstatus
#与360安全页面加密一致
def md5(str):
    str=str.encode('utf-8')
    m=hashlib.md5()
    m.update(str)
    return m.hexdigest()

def login_trx(user,passwd):
    # url="https://89.36.16.47/cgi/maincgi.cgi?Url=Index"
    # headers_cookie={
    #     "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)"
    # }
    # udata={
    #     'username': user,
    #     'passwd': passwd,
    #     'loginSubmitIpt':'',
    # }
    # s=requests.Session()
    # res=s.post(url=url,headers=headers_cookie,data=udata,timeout=5,verify=False)
    net=sql_select('trx')
    ctime=datetime.datetime.now()
    nt=datetime.timedelta(days=-10)
    etime=ctime+nt
    strctime=ctime.strftime("%Y-%m-%d")
    stretime=etime.strftime("%Y-%m-%d")
    reslist=[]
    for i in net:
        mongo_table=i[0]
        url=i[4]
        user=i[8]
        passwd=i[9]
        ip=i[10]        
        loginurl='https://'+ip+"/cgi/maincgi.cgi?Url=Index"
        headers_cookie={
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)"
        }
        udata={
            'username': user,
            'passwd': passwd,
            'loginSubmitIpt':'',
        }
        s=requests.Session()
        res=s.post(url=loginurl,headers=headers_cookie,data=udata,timeout=5,verify=False)

        url=url.replace('[ctime]',strctime)
        url=url.replace('[etime]',stretime)  
        strstatus=get_status_res(url,s)
        reslist=reslist+htmltable_json(strstatus)        
        s.close()
    if (type(reslist).__name__=='list'):
        sql_into_mongo('netMonitor',mongo_table,reslist)
    else:
        print('not is dict')
def netmong_mysql(dbname,tablename):
    global database
    global myclient
    loglist=[]  
    #取mango数据导入mysql
    try:
        mydb=myclient[dbname]
        collist=mydb.list_collection_names()
        if tablename in collist:
            coll=mydb[tablename]
            for item in coll.find({},{"ip":1,"mac":1,"createAt":1,"_id":0}):
                loglist.append([item['ip'],item['mac'],item['createAt'].strftime("%Y-%m-%d %H:%M:%S")])
        myclient.close()
    except:
        pass
    # #清空表
    # connmysqld=pymysql.connect(**database)
    # cursormysqld=connmysqld.cursor()
    # sqlmysqld='TRUNCATE TABLE pc_live'
    # try:
    #     cursormysqld.executemany(sqlmysqld)
    # except:
    #     print('Mysql del Faile')
    #     pass
    # cursormysqld.close()
    # connmysqld.commit()
    # connmysqld.close() 
    #取mango数据导入mysql
    connmysql=pymysql.connect(**database)
    cursormysql=connmysql.cursor()
    sqlmysql='insert into pc_live(ip,mac,createAt) values(%s,%s,%s)'
    try:
        sqlmysqld='TRUNCATE TABLE pc_live'
        cursormysql.execute(sqlmysqld)
        cursormysql.executemany(sqlmysql,loglist)
    except:
        print('Mysql insert Faile')
        pass
    cursormysql.close()
    connmysql.commit()
    connmysql.close()  
def htmltable_json(html):
    res_dict=[]    
    try:
        re_table=re.compile('<table width="100%" id="tableId">(.*?)</table>',re.S)
        re_tr=re.compile('<tr.*?>(.*?)</tr>',re.S)
        re_value=re.compile('value="(.*?)"',re.S)
        res_table=re.findall(re_table,html)
        res_tr=re.findall(re_tr,res_table[0])
        res_swjg=sql_select('360',False)
        for i in res_tr[1:]:
            res_one={}
            res_value=re.findall(re_value,i)
            res_values=res_value[0].split("|")
            res_group=''
            for j in res_swjg:
                if res_values[0].find(j[0])>=0:
                    res_group=j[2]
                    break
            res_one['sgroup']=res_group
            res_one['sip']=res_values[0]
            res_one['sport']=res_values[1]
            res_one['dip']=res_values[2]
            res_one['dport']=res_values[3]
            res_one['proxy']=res_values[4]
            res_dict.append(res_one)        
    except:
        print('sprider table error')
    # res['list']=
    return res_dict

#主程序执行
def spider_app(appname,run=True,times=360):
    while run:
        if appname.find('360')>=0:
            login_req('qiandongnan','qdndzswzx6620')
            print('360 spider ok')
        if  appname.find('trx')>=0:
           login_trx('superman','fireA2012')
           print('trx spider ok')
        if appname.find('netmon')>=0:
            netmong_mysql('netMonitor','pc_live')
            print('netmon export mysql ok')
        if work_time():
            sleep(times)
        else:
            run=False

if __name__ == "__main__":    
    login('http://lab1.xseclab.com/','http://lab1.xseclab.com/xss2_0d557e6d2a4ac08b749b61473a075be1/index.php')