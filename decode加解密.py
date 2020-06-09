
#!/usr/bin/python
# -*- coding: utf-8 -*-
# 导入 base64模块
import base64
from base64 import *
import re
import exrex
from collections import OrderedDict #排序
# import pycuda.autoinit
# import pycuda.driver as drv
# from pycuda.compiler import SourceModule

#字符串大小写转换
def dfs(res, arr, pos):
    res.append(''.join(arr))
    i = pos
    for i in range(i, len(arr)):
        if arr[i] <= 'Z' and arr[i] >= 'A':
            arr[i] = arr[i].lower()
            dfs(res, arr, i + 1)
            arr[i] = arr[i].upper()

def decode_base64(stro):
    arr = list(stro)
    res = []
    dfs(res, arr, 0)
    res_decode = map(b64decode, res)
    for i in res_decode:
        if re.findall(r'\\x', repr(i)):
            continue
        else:
            print (i)
#批量同时替换字符1
def multiple_replace(text, adict):  
     rx = re.compile('|'.join(map(re.escape, adict)))  
     def one_xlat(match):  
           return adict[match.group(0)]  
     return rx.sub(one_xlat, text) 
#批量同时替换字符2
def make_xlat(*args, **kwds):  
     adict = dict(*args, **kwds)  
     rx = re.compile('|'.join(map(re.escape, adict)))  
     def one_xlat(match):  
           return adict[match.group(0)]  
     def xlat(text):  
           return rx.sub(one_xlat, text)  
     return xlat 
#字符替换密码——取密文字符对应特征值,defdd(密文，明文)
def defdd(pass_str,m_str):
    dic={}
    if len(pass_str)==len(m_str):
        for i in range(len(pass_str)):
            xx={pass_str[i]:m_str[i]}
            dic.update(xx)
    return dic
#返回不确定的密文对应特征值，默认为base64
def res_passwd(dic,basedic='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/'):
    res=''
    for i in basedic:
        # if dic.setdefault(str(i),'pgy')=='pgy':
        #     res=res+i
        if dic.get(i):
            pass
        else:
            res=res+i
    return res        
#取密文字符对应特征值返回列表
def s_list(str1,str2):
    lists=[]
    if len(str1)==len(str2):
        for i in range(len(str1)):
            # xx={str2[i]:str1[i]}
            # dic.update(xx)
            lists.append(str2[i]+':'+str1[i])
    return lists
#字典包生成列表
def list_dict(list_s,s,dict_type):
    dict_s=list(exrex.generate(dict_type))
    res_list=[]
    for list_s_n in list_s:
        for dict_s_n in dict_s:
            res_list.append(list_s_n.replace(s,dict_s_n))
    return res_list
#生成自定义字典包[['0',dic],['1',dic],['2',dic]]
def dic_create(s,input_list):
    list_res=[s]
    for n in range(len(input_list)):
        ns='-'+input_list[n][0]+'-'
        nre=input_list[n][1]
        list_res=list_dict(list_res,ns,nre)     # E-G-I   
    return list_res
#判断是否符合base64解密后的明文
def is_base64(textn):
    res=False
    rex=r'[\\x%?!><=./$\]"]+'
    textm=''
    try:
        textm=base64.b64decode(textn).decode('ascii')
    except:
        res=False
    else:
        res=True
        rest=re.search(rex,textm)
        if rest:
            res=False
        else:
            res=True
    return res
#分组返回合法的base64对应的值
def is_base64_pwd(text,dic):
    # if type(len(str)/4)==int:
    res=[text,'']
    rex=r'[~!@#$%^&*\]"]+'
    d='~!@#$%^&*'
    s=[]
    lst=cut_text(text,4)
    for i in range(len(d)):
        m=''
        for j in lst:
            rest=re.search(rex,j)
            if rest and j.find(d[i])>=0:
                # for l in range(len(rest.group())):
                if len(rest.group())==1:
                    for k in list(dic)[1:-1]:
                        # a=j.replace(d[i],k)
                        a=j.replace(rest.group()[0],k)
                        if is_base64(a):
                            print(a)
                            m=m+k
                elif len(rest.group())>1:
                    m=str(dic[1:-1])
                if m!='':
                    m="".join(OrderedDict.fromkeys(m))
                    n=rest.group()
                    n=n.replace(r'!#','3')
                    n=n.replace(r'~','0')
                    n=n.replace(r'!','1')
                    n=n.replace(r'@','2')
                    n=n.replace(r'#','3')
                    n=n.replace(r'$','4')
                    n=n.replace(r'%','5')
                    n=n.replace(r'^','6')
                    n=n.replace(r'&','8')
                    s.append(n+',['+m+']')                    
    res[0]=res[0].replace('~','-0-')
    res[0]=res[0].replace('!','-1-')
    res[0]=res[0].replace('@','-2-')
    res[0]=res[0].replace('!#','-3-')
    res[0]=res[0].replace('#','-3-')
    res[0]=res[0].replace('$','-4-')
    res[0]=res[0].replace('%','-5-')
    res[0]=res[0].replace('^','-6-')
    res[0]=res[0].replace('&','-7-')
    s=list(dict.fromkeys(s))#除去list重复值
    t=[]
    for x in range(len(s)):        
        t.append(s[x].split(','))
    res[1]=t

    #     for 
    # for i in range(len(lst)-1):
    #     if lst[i].find('~!@#$%')>=0:
    #         for j in list(dic)[1:-1]:
    #             a=lst[i].replace('?',j)
    #             if is_base64(a):
    #                 s=s+j
    #         res.append('-'+str(i)+'-','['+s+']')
    
    return res

#解密
def my_decode(s,input_list):
    dic=dic_create(s,input_list)
    reslist=[]
    for a in dic:
        # try:
        textn=base64.b64decode(a)
        textn=str(textn)
        ret=re.match('b\'flag\\{(.*)\\}\'$',textn)
        # ret=True
        rex=r'[\\x%?!><=./$\]"]+'
        if ret:
            rest=re.search(rex,textn)
            if rest:
                pass
            else:
                # print(a)
                # print ('sucess--'+textn)
                reslist.append(a)
    return reslist
        
        # # else:
        #     print (a)
        # finally:
        #     print('error---'+DD)
#按照固定长度分割字符串
def cut_text(text,lenth): 
    textArr = re.findall('.{'+str(lenth)+'}', text) 
    textArr.append(text[(len(textArr)*lenth):]) 
    return textArr
if __name__ == '__main__':
    basedic='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/'
    pp='uLdAuO8duojAFLEKjIgdpfGeZoELjJp9kSieuIsAjJ/LpSXDuCGduouz'
    p='pTjMwJ9WiQHfvC+eFCFKTBpWQtmgjopgqtmPjfKfjSmdFLpeFf/Aj2ud3tN7u2+enC9+nLN8kgdWo29ZnCrOFCDdFCrOFoF'#密文
    o='YXNobGtqIUBzajEyMjMlXiYqU2Q0NTY0c2Q4NzlzNWQxMmYyMzFhNDZxd2prZDEySjtESmpsO0xqTDtLSjg3MjkxMjg3MTM'#明文
    old_dic=defdd(o,p)
    dic='['+res_passwd(old_dic)+']'
    old_list=s_list(o,p)
    # text='ZmxhZ3sxZTNhMm?lN?0xYzGyLT?mNGYtOW?yZ??hNGFmYWXkZj?xZTZ?'
    text='ZmxhZ3sxZTNhMm~lN!0xYz@yLT~mNGYtOWIyZ!#hNGFmYW$kZj@xZTZ%'#6个特殊符号代替（~!@#$%^&*）
    respwd=is_base64_pwd(text,dic)
    # dic='[ACHJKPRVefnuvw156789+/]'    
    # dic='[AHJKPRVefnuvw5678+/]'
    res=my_decode(respwd[0],respwd[1])
    # res=my_decode('ZmxhZ3sxZTNhMm-0-lN-1-0xYz-2-yLT-0-mNGYtOWIyZ-1--3-hNGFmYW-4-kZj-2-xZTZ-5-',[['0',dic],['1',dic],['2',dic],['3',dic],['4',dic],['5',dic]])
    # res=my_decode('ZmxhZ3sxZTNhMm-0-lNC0xYz-1-yLT-0-mNGYtOWIyZC1hNGFmYW-2-kZj-1-xZTZ9',[['0',dic],['1',dic],['2',dic]])
    #  生成新的替代字幕对应值  
    new_list=[]
    for i in res:
        # new_dic.update(defdd(pp,i))
        ok=True
        n=s_list(pp,i)
        n=list(dict.fromkeys(n))
        x=str(n)
        for j in basedic:
            if x.count(j+':')>1:
                ok=False
                break
        if ok:
            new_list.append(i)


    rex=r'flag\{.{8}-.{4}-.{4}-.{4}-.{12}\}'
    pwd=[]
    for b in new_list:
        # b=multiple_replace(pp,dic_n)\
        flag=base64.b64decode(b.encode('utf-8')).decode('utf-8')
        rest=re.search(rex,flag)
        if rest:
            pwd.append(rest.group())  
            print(rest.group())     
    pass
    
    # my_decode('ZmxhZ3sxZTNhMm-0-lN-1-0xYz-2-yLT-0-mNGYtOWIyZ-1--3-hNGFmYW-5-kZj-2-xZTZ-4-',[['0',dic],['1',dic],['2',dic],['3',dic],['4',dic],['5',dic]])
    # my_decode('ZmxhZ3sxZTNhMm_0_lN_5_0xYz_3_yLT_0_mNGYtOWyZ_1__2_hNGFmYWXkZj_3_xZTZ_4_',[['0',dic],['1',dic],['2',dic],['3',dic],['4',dic],['5',dic]])
    #按要求生成密码字典，3个随机变量，4个值，其中_0_=_0_，需要随机变量想等,超过4个暴力超1千万条
    # my_decode('ZmxhZ3sxZTNhMm_0_lNI0xYz_3_yLT_0_mNGYtOWIyZ_1__2_hNGFmYWXkZj_3_xZTZ_5_',[['0','[0-9a-zA-Z]'],['1','[0-9a-zA-Z]'],['2','[0-9a-zA-Z]'],['3','[0-9a-zA-Z]']])
    # text='ashlkj!@sj1223%^&*Sd4564sd879s5d12f231a46qwjkd12J;DJjl;LjL;KJ8729128713'
    # mtext='pTjMwJ9WiQHfvC+eFCFKTBpWQtmgjopgqtmPjfKfjSmdFLpeFf/Aj2ud3tN7u2+enC9+nLN8kgdWo29ZnCrOFCDdFCrOFoF='
    # b64text=base64.b64encode(text.encode('utf-8')).decode('ascii')
    # dic=defdd(b64text,mtext)
    # multiple_replace(mtext, dic)
    # defdd('YXNobGtqIUBzajEyMjMlXiYqU2Q0NTY0c2Q4NzlzNWQxMmYyMzFhNDZxd2prZDEySjtESmpsO0xqTDtLSjg3MjkxMjg3MTM','pTjMwJ9WiQHfvC+eFCFKTBpWQtmgjopgqtmPjfKfjSmdFLpeFf/Aj2ud3tN7u2+enC9+nLN8kgdWo29ZnCrOFCDdFCrOFoF',
    # 'uLdAuO8duojAFLEKjIgdpfGeZoELjJp9kSieuIsAjJ/LpSXDuCGduouz')
    # mustr('uLdAuO8duojAFLEKjIgdpfGeZoELjJp9kSieuIsAjJ/LpSXDuCGduouz')
    # my1('ZmxhZ3sxZTNhMmElNI0xYzGyLTEmNGYtOWIyZIshNGFmYWXkZjGxZTZ9')