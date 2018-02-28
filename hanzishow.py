# -*- coding: utf-8 -*-

from radical import Radical
import os, re, sys
from langconv import *

def Simplified2Traditional(sentence):
    '''
    将sentence中的简体字转为繁体字
    :param sentence: 待转换的句子
    :return: 将句子中简体字转换为繁体字之后的句子
    '''
    sentence = Converter('zh-hant').convert(sentence)
    return sentence

if __name__ == '__main__':
    radical = Radical()

#duti_dict={}
#优先显示偏旁列表 26个常用偏旁 出现在60%汉字
pry_pp=['人','亻','女','忄','犭','纟','走','辶','鸟','鱼','钅','月','肉','目','食','饣','口','足','虫','木','言','讠','扌','氵','火','灬','土','艹','日','山','疒','日','石']

#偏旁笔画
dutizi={}
#汉字起源图片 {汉字:汉字图片url}
hzorig={}
#汉字偏旁 {汉字偏旁:汉字}
hzpp={}
#汉字笔画
hzbh={}
#偏旁笔画 笔画:偏旁列表
ppbh={}
#具有汉字起源图片的汉字字典,来自www.xiuwenyuan.com
hanzi_dict="hanzi_dict.txt"
#独体字文件 包含笔画顺序独体字
dutizi_source="dutihanzi.txt"
#html5 md slides 头部内容
header='''---
layout: reveal
title:  "汉字偏旁部首-%s-%03d"
date:   2017-1-24
author: "升烟"
desc: "穿越时空的汉字旅行"
keywords: "记忆 汉字 说文"
categories: [zhongwen]
reveal_theme: "blood.css"
tags: [Jalpc,Jekyll]
icon: icon-html
---

'''

#控制每个slides能加载多少个汉字
PAGE_MAX=150
PP_MAX=10
#对文件序号计数,分类归零
page_no=1
#每个Slide加载的汉字计数
page_count=0
#已输出列表
donehzlist=[]
#无法找到起源图片列表，即生僻字
wildhzlist=[]
#每个输出文件加载汉字计数器

#第一个参数为主题，第二个参数为计数
outputfile='%s/2017-1-1-汉字起源-%s-%03d.html'

#Load data from file
def loaddDictFromFile():
    #加载汉字库入字典
    if os.path.isfile(hanzi_dict):
        f = open (hanzi_dict)
        for line in f:
            if re.match("^#.*$",line) or not line.strip():
                continue
            line=line.decode('utf-8')
            hz, tmp, png = line.partition(u"=")
            hzorig[hz]=png
        f.close()
    #加载笔画偏旁 入字典
    if os.path.isfile(dutizi_source):
        f = open(dutizi_source)
        num=0
        for line in f:
            if re.match(u"^#.*$", line) or not line.strip():
                continue
            line = line.decode("utf-8")
            m_num = re.match(u'(\d+) 画', line)

            if m_num:
                num=int(m_num.group(1))
                #print "find the number:" +str(num)
                continue
            m_hz=re.findall(u'[\u4e00-\u9fa5]', line)
            if m_hz:
                if num in dutizi:
                    lst=dutizi[num]
                    lst.extend(m_hz)
                    dutizi[num]=lst
                else:
                    dutizi[num]=m_hz
        #print hzorig[u'我']
    #print len(dutizi)

def loadhz_pp_bh_fromdict(hzdict):
    i = 0
    for k in hzdict:
        i=i+1
        pp=radical.get_radical(k.encode('utf-8'))
        bh=int(radical.get_stroke(k.encode('utf-8')))
        pp=pp.decode('utf-8')
        if pp in hzpp:
            lst=hzpp[pp]
            lst.append(k)
            hzpp[pp]=lst
        else:
            #print pp
            lst=[]
            lst.append(k)
            hzpp[pp]=lst
        #if i < 5:
        if bh in hzbh:
            lst=hzbh[bh]
            lst.append(k)
            hzbh[bh]=lst
        else:
            lst=[]
            lst.append(k)
            hzbh[bh]=lst
    for k in hzpp:
        bh= int(radical.get_stroke(k.encode('utf-8')))
        if bh in ppbh:
            lst=ppbh[bh]
            lst.append(k)
            ppbh[bh]=lst
        else:
            ppbh[bh]=[k]
    #print len(hzpp)
    #print len(hzbh)
    #print len(ppbh)

#输出以某个偏旁代表的所有汉字起源的Markdown
#catag汉字的类别,见hzcategories
#pp偏旁 (unicode)
#max 单个偏旁允许输出的汉字
def hanzimdoutput(categ , pp, mx=PP_MAX):
    global page_count,f,page_no
    if pp not in donehzlist:
        if page_count < PAGE_MAX:
            counter=0
            #print pp.encode('utf-8') + ":" + str(pp in hzpp)
            if pp in hzorig:
                f.write("# " + pp.encode('utf-8') + "\n\n")
                f.write("![normal](" + hzorig[pp] +")" + "\n\n")
            if pp in hzpp:
                #print "pp:" + pp
                if pp not in hzorig:
                    f.write("# " + pp.encode('utf-8') + "\n\n")
                    f.write("--\n\n")
                else:
                    f.write("--\n\n")
                for v in hzpp[pp]:
                    #print 'v:' + v.encode('utf-8')
                    if v in donehzlist:
                        continue
                    if v in hzorig and counter < mx:
                        donehzlist.append(v)
                        f.write("![big ](" + hzorig[v] +")" + "\n\n")
                        counter=counter+1
                        page_count=page_count+1
                    elif v not in hzorig:
                        print j.encode('utf-8') + " 不在汉字起源库中,自动跳过！"
                        wildhzlist.append(v)
                    #if not the last one
                    if counter < len(hzpp[pp]) and counter < mx:
                        f.write("--\n\n")
                donehzlist.append(pp)
            else:
                if pp.encode('utf-8') not in pry_pp and pp not in hzpp and pp not in hzorig:
                    print pp.encode('utf-8') + " 不在汉字起源库中,自动跳过！"
                    wildhzlist.append(pp)
            f.write("---\n\n")
        else:
            f.close()
            #Open a new file
            page_no = page_no+1
            f=open(outputfile % (outputpath,categ,page_no), "w")
            f.write(header % (categ, page_no))
            page_count=0
            #从新调用
            hanzimdoutput(categ, pp, mx)


def resetcounter():
    global page_no,page_count,pp_count
    page_no=1
    page_count=0
    pp_count=0

#加载汉字笔画数量dict
def loadhanzibhfromdict(hzdict):
    print "not define yet"

def printulist(l):
    for v in l:
        if isinstance(v,unicode):
            print v.encode('utf-8'),
        else:
            print v,
baseouputpath="./"
if len(sys.argv) == 2:
    baseouputpath=sys.argv[1]

outputpath=baseouputpath +'_slides'

#控制每个偏旁能加载多少个汉字
loaddDictFromFile()
loadhz_pp_bh_fromdict(hzorig)

hzcatagory=['常用偏旁', '独体字偏旁','其他偏旁','生僻字', '独体字汉字']

#1展示pry 偏旁
f=open(outputfile % (outputpath, hzcatagory[0], page_no) , "w")
f.write(header % (hzcatagory[0], page_no))

f.write("## 26个常用偏旁出现于60%汉字中\n\n")
f.write("---\n\n")
for i in pry_pp:
    ui=i.decode("utf-8")
    hanzimdoutput(hzcatagory[0], ui, PP_MAX)

f.close()
#2展示独体字 偏旁
resetcounter()
f=open(outputfile % (outputpath, hzcatagory[1], page_no), "w")
f.write(header % (hzcatagory[1], page_no))
f.write('# 独体字\n')
f.write('### 按照笔画顺序\n\n')
f.write('---\n\n')
for i in dutizi:
    f.write('# ' + str(i) + '比画\n\n')
    f.write('---\n\n')
    for j in dutizi[i]:
        #print j + str(isinstance(j,unicode))
        hanzimdoutput(hzcatagory[1],j,PP_MAX)

f.close()

#3展示其他偏旁
resetcounter()
f=open(outputfile % (outputpath, hzcatagory[2], page_no), "w")
f.write(header % (hzcatagory[2], page_no))
f.write('# 其他偏旁-' + str(page_no) + '\n\n')
f.write('---\n\n')
for p in hzpp:
    #print p + str(isinstance(p, unicode))
    hanzimdoutput(hzcatagory[2],p,PP_MAX)

f.close()

#4 其它生僻字()
resetcounter()
f=open(outputfile % (outputpath, hzcatagory[3], page_no), "w")
f.write(header % (hzcatagory[3], page_no))
f.write('# 生僻字\n\n')
f.write('### 没有找到起源图片,共' + str(len(wildhzlist)) + '个\n\n')
f.write('---\n\n')
for i in wildhzlist:
    f.write('# ' + i.encode('utf-8') + '\n\n---\n\n' )
f.close()

#4展示独体汉字
f=open(outputfile % (outputpath, hzcatagory[4], 1) , "w")
f.write(header % (hzcatagory[4], 1))

for i in dutizi:
    n=0
    if i>0:
        f.write('# 笔画' + str(i) + '\n\n--\n\n')
        for j in dutizi[i]:
            if j in hzorig:
                f.write("![big ](" + hzorig[j] +")" + "\n\n")
                n=n+1
            if n<len(dutizi[i]):
                f.write("--\n\n")
        f.write("---\n\n")

#5 输出 Markdown blog文档:
blog_header='''---
layout: post
title:  "汉字字源"
date:   2017-01-31
desc: "从汉字起源重新认识中国字"
keywords: "说文解字 许慎 汉字 起源"
categories: [zhongwen]
tags: [汉字,语文]
icon: icon-html
---

'''
outputblogpath=baseouputpath + '_posts/'
f=open(outputblogpath + "2017-1-31-汉字起源.md" , "w")
f.write(blog_header)
f.write('# 目录\n')
f.write('## [独体字](#dtz)\n' )
f.write('## [偏旁顺序](#pp)\n' )
f.write('## [笔画顺序](#bh)\n' )
f.write('----\n')
f.write('# <a name="dtz">独体字</a>\n')
for i in dutizi:
    f.write("### " + str(i)+ '画\n')
    for j in dutizi[i]:
        if j in hzorig:
            f.write('[' + j.encode('utf-8') + '('+ Simplified2Traditional(j).encode('utf-8') +')](' + hzorig[j].encode('utf-8') +') ')
    f.write('\n')
f.write('----\n')
f.write('# <a name="pp">偏旁顺序</a>\n')
for m in ppbh:
    for i in ppbh[m]:
        f.write('## ' + str(i.encode('utf-8')) + '字旁['+ str(m) + ']\n')
        for j in hzpp[i]:
            f.write('[' + j.encode('utf-8') + '('+ Simplified2Traditional(j).encode('utf-8') +')](' +hzorig[j].encode('utf-8') +') ')
        f.write('\n')

f.write('----\n')
f.write('# <a name="bh">笔画顺序</a>\n')
for i in hzbh:
    f.write('## ' + str(i) + '画\n')
    for j in hzbh[i]:
        f.write('[' + j.encode('utf-8') + '('+ Simplified2Traditional(j).encode('utf-8') +')](' +hzorig[j].encode('utf-8') +') ')
    f.write ('\n')

f.close()
#radical.save()

def debuginfo():
    for k, v in dutizi.iteritems():
        printulist(v)

    print "\n"
    for k,v in hzpp.iteritems():
        print k.encode('utf-8'),

    print "\n相同:\n"

    for k, v in dutizi.iteritems():
        for i in v:
            if i in hzpp:
                print i.encode("utf-8"),

    print "\n不同:\n"
    for k, v in dutizi.iteritems():
        for i in v:
            if i not in hzpp:
                print i.encode("utf-8"),
