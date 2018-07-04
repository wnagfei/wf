# _*_coding:utf-8_*_
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import threading,time
from urllib import request
import  re
import  urllib
from lxml import etree
def getMain(secpage,):
    header={
           'Accept': 'textml,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Cookie': '__51cke__=; Hm_lvt_cab9571626f709d8541b6dc32fb5ceaa=1529040738; __tins__19069144=%7B%22sid%22%3A%201529040738039%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201529042604042%7D; __51laig__=3; Hm_lpvt_cab9571626f709d8541b6dc32fb5ceaa=1529040804',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            }
    nextheader = {
    }
    req = urllib.request.Request(secpage, headers=nextheader)
    numhtml = urllib.request.urlopen(req)
    numhtml = numhtml.read().decode('utf8')
    #print(numhtml)
    thirdPage = etree.HTML(numhtml)
    thirdPage = thirdPage.xpath("//ul[@class='a-b']//a/@href")
    #print(thirdPage)
    getAll(thirdPage,20)
def getAll(thirdPage, threads_max_count):
    nextheader={
        'Accept': 'textml,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    #print(thirdPage)
    for th in thirdPage:
        try:
            print(th)
            req = urllib.request.Request(th, headers=nextheader)
            numhtml = urllib.request.urlopen(req)
            numhtml = numhtml.read().decode('utf8')
            secnum = etree.HTML(numhtml)
            secnum = thirdPage.xpath("//ul[@class='scan']//a/@href")
            #print(secnum)
            for sec in secnum:
                req = urllib.request.Request(sec, headers=nextheader)
                numx = urllib.request.urlopen(req)
                numx = numhtml.read().decode('utf8')
                # secx = etree.HTML(numhtml)
                # secx = thirdPage.xpath("//ul[@class='scan']//a/@href")
                reg = r'src="(.+?\.jpg)"'
                imgre = re.compile(reg)
                imglist = re.findall(imgre, numx)
                namereg = r'(?<=\balt=")[^"]*(?="\s+)'
                name=re.compile(namereg)
                Allname=re.findall(name,numx)
                Allname = "".join(Allname)
           #   print(imglist)
            #  print(Allname)
                for imgurl in imglist:
                    pool = ThreadPool(4)
                    pool = ThreadPool(urllib.request.urlretrieve(imgurl, 'd://%s.jpg' % Allname))
                    pool.close()
                    pool.join()
        except:
            continue;
if __name__ == '__main__':
    header = {
        'Accept': 'textml,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Cookie': '__51cke__=; Hm_lvt_cab9571626f709d8541b6dc32fb5ceaa=1529040738; __tins__19069144=%7B%22sid%22%3A%201529040738039%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201529042604042%7D; __51laig__=3; Hm_lpvt_cab9571626f709d8541b6dc32fb5ceaa=1529040804',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    nextheader = {
    }
    MainPage = 'http://zhonghuabook.com/book-scan/'
    req = urllib.request.Request(MainPage, headers=header)
    html = urllib.request.urlopen(req)
    html = html.read().decode('utf8')
    nexthtml = etree.HTML(html)
    secPage = nexthtml.xpath("//ul[@class='scan']//a/@href")
    threads = []
    for secopage in  secPage:
        t = 'http'
        result = t in secopage
        if(result):
            s = threading.Thread(target=getMain, args=(secopage,))
            threads.append(s)
        else:
            secopage = "http://zhonghuabook.com"+secopage
            #print(secopage)
            s = threading.Thread(target=getMain, args=(secopage,))
            threads.append(s)
        urls = range(len(secPage));
    for i in urls:
        threads[i].start()
    for i in urls:
        threads[i].join()
