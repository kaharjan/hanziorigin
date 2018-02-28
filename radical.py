# encoding=utf-8

import re
import csv
import urllib2
from bs4 import BeautifulSoup

class Radical(object):
    dictionary_filepath = 'xinhua.csv'
    baiduhanyu_url = 'http://hanyu.baidu.com/zici/s?ptype=zici&wd=%s'

    def __init__(self):
        self.read_dictionary()
        self.origin_len = len(self.dictionary)

    def read_dictionary(self):
        self.dictionary = {}

        file = open(self.dictionary_filepath, 'rU')
        reader = csv.reader(file)

        for line in reader:
            #如果笔画数不存在
            if len(line)<3 or line[2]:
                line.append("0".decode('utf-8'))
                #result = self.get_result_from_baiduhanyu(line[0].decode('utf-8'))
                #if result:
                #    line.append(result[1])
                #else:
                #    print line[0] + " 未查询到笔画!"
                #    line.append("0".decode('utf-8'))
            self.dictionary[line[0].decode('utf-8')] = [line[1].decode('utf-8'),line[2].decode('utf-8')]
        file.close()

    def write_dictionary(self):
        file_obj = open(self.dictionary_filepath, 'wb')

        writer = csv.writer(file_obj)
        for word in self.dictionary:
            writer.writerow([word.encode('utf-8'),self.dictionary[word][0].encode('utf-8'),self.dictionary[word][1].encode('utf-8')])

        file_obj.close()

    def get_radical(self,word):
        word = word.decode('utf-8')

        if word in self.dictionary:
            result = self.dictionary[word][0]
        else:
            result = self.get_result_from_baiduhanyu(word)
            self.add_in_dictionary(word,result)
        return result[0].encode('utf-8')

    def get_stroke(self,word):
        word = word.decode('utf-8')

        if word in self.dictionary and int(self.dictionary[word][1])!=0:
            result = self.dictionary[word]
        else:
            result = self.get_result_from_baiduhanyu(word)
            if word not in self.dictionary:
                self.add_in_dictionary(word,result)
        if result and len(result)>1:
            return result[1].encode('utf-8')
        else:
            print "加载笔画失败！"
            return "0"

    def post_baidu(self,url):
        url=url.encode('utf-8')
        #print url
        try:
            timeout = 5
            request = urllib2.Request(url)
            #伪装HTTP请求
            request.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
            request.add_header('connection','keep-alive')
            request.add_header('referer', url)
            # request.add_header('Accept-Encoding', 'gzip')  # gzip可提高传输速率，但占用计算资源
            response = urllib2.urlopen(request, timeout = timeout)
            html = response.read()
            #if(response.headers.get('content-encoding', None) == 'gzip'):
            #    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
            response.close()
            return html
        except Exception as e:
            print 'URL Request Error:', e
            return None

    def anlysis_radical_stroke_from_html(self,html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        li = soup.find(id="radical")
        if li:
            radical = li.span.contents[0]
        else:
            radical =''
        li = soup.find(id="stroke_count")
        if li:
            stroke = li.span.contents[0]
        else:
            #print html_doc
            print "未见笔画字段!"
            stroke="0"

        return (radical,stroke)

    def add_in_dictionary(self,word,result):
        # add in file
        if result and len(result) > 1:
            file_object = open(self.dictionary_filepath,'a+')
            file_object.write(word.encode('utf-8')+','+result[0].encode('utf-8')+ ','+ result[1].encode('utf-8') +'\r\n')
            file_object.close()
            # refresh dictionary
            self.read_dictionary()
        else:
            print word.encode('utf-8')+ "偏旁笔画对象不存在！"

    def get_result_from_baiduhanyu(self,word):
        url = self.baiduhanyu_url % word
        html = self.post_baidu(url)

        if html == None:
            return None

        result = self.anlysis_radical_stroke_from_html(html)
        if result != None and len(result) == 2:
            self.dictionary[word] = [result[0], result[1]]

        return result

    def save(self):
        #if len(self.dictionary) > self.origin_len:
        self.write_dictionary()

if __name__ == '__main__':
    r = Radical()
    print r.get_radical('棶')
    r.save()
