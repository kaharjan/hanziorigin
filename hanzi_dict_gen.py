# -*- coding: utf-8 -*-

import urllib2
import re
import sys



def grab_web_page(page_num):
    req = urllib2.Request("http://www.xiuwenyuan.com/ziyuan/daquan/" + page_num + ".html")
    response = urllib2.urlopen(req)
    page_content = response.read()
    return page_content.decode('gbk')

def parser_dict(html_string, _file1, _file2, _dest_folder):
    #pattern = re.compile(r'<li><a href="http://www\.xiuwenyuan\.com/ziyuan/([a-zA-Z0-9]{6})\.html">(.+)</a></li>')
    pattern = re.compile(u'http://www\.xiuwenyuan\.com/ziyuan/([a-zA-Z0-9]{6})\.html">([\u4e00-\u9fa5]+)</a>')
    #pattern = re.compile(u'[\u4e00-\u9fa5]+</a>')

    for m in re.findall(pattern, html_string):
        u_string=m[1]+ "=http://www.xiuwenyuan.com/zi/ziyuanimg/" + m[0] + ".png\n"
        _file1.write(u_string.encode('utf-8'));
        u_string="wget http://www.xiuwenyuan.com/zi/ziyuanimg/" + m[0] + ".png -O " + _dest_folder + m[0] + ".png\n"
        _file2.write(u_string.encode('utf-8'));

def generate_hanzi_dict():
    #_f = open("test.html", 'r')
    page_list=["index", "2", "3", "4", "5"]
    #_tmp_file = open("hanziorigin.html", "w+")
    _output_f1=open("hanzi_dict.txt", 'w+')
    _output_f2=open("download.sh", 'w+')
    _dest_folder="/tmp/download/"
    _output_f2.write("mkdir -p " + _dest_folder + "\n")
    for i in page_list:
        line = grab_web_page(i)
        #_tmp_file.write(line + "\n")
        #print line
        #line = line.encode('unicode')
        parser_dict(line,  _output_f1, _output_f2, _dest_folder)
    _output_f1.close
    _output_f2.close
    #_tmp_file.close


def generate_dutizi():
    _f = open ("dutihanzi.txt", "r")
    _f.close()


generate_hanzi_dict()
