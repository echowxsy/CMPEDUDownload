#!/usr/local/bin/python3
# coding=utf-8

import requests
import json
import threading
import sys
import os
import time


class MulThreadDownload(threading.Thread):
    def __init__(self, url, startpos, endpos, f):
        super(MulThreadDownload, self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f

    def download(self):
        print("[LOG] start thread: [%s] at %s" % (self.getName(),
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        headers = {
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'DNT': '1',
            'Accept-Encoding': 'identity',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://cmpebooks.s3.cn-north-1.amazonaws.com.cn/pdfReader/generic/build/pdf.worker.js',
            'Connection': 'keep-alive',
            'Range': 'bytes=%s-%s' % (self.startpos, self.endpos)
        }
        res = requests.get(self.url, headers=headers)
        # res.text 是将get获取的byte类型数据自动编码，是str类型， res.content是原始的byte类型数据
        # 所以下面是直接write(res.content)
        self.fd.seek(self.startpos)
        self.fd.write(res.content)
        print("[LOG] stop thread: [%s] at %s" % (self.getName(),
                                                 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        # f.close()

    def run(self):
        self.download()


def getBookCategoryInfo(code, page, limit):
    baseAPI = "http://ebooks.cmanuf.com/getBookCategoryInfo"
    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://ebooks.cmanuf.com',
        'Referer': 'http://ebooks.cmanuf.com/all?id=1&type=2&code=AC16',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    payload = "code="+code+"&date=&page="+page+"&px=desc&limit="+limit
    response = requests.request("POST", baseAPI, headers=headers, data=payload)
    return json.loads(response.text)


def isCmpebooks(imgUrl):
    index = imgUrl.find('cmpebooks.s3.cn-north-1.amazonaws.com.cn')
    if index > 0:
        return True
    else:
        return False


def genPDFUrl(imgUrl):
    pdfUrl = imgUrl.replace('/Cover/', '/PDF/')
    pdfUrl = pdfUrl.replace('Cover1.jpg', '2.pdf')
    return pdfUrl


def downloadPdf(filename, url):
    headers = {
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'DNT': '1',
        'Accept-Encoding': 'identity',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://cmpebooks.s3.cn-north-1.amazonaws.com.cn/pdfReader/generic/build/pdf.worker.js',
        'Connection': 'keep-alive'
    }
    filesize = int(requests.head(
        url, headers=headers).headers['Content-Length'])
    print("[LOG] %s filesize: %.2fMB" % (filename, filesize/(1024*1024)))
    # 线程数
    threadnum = 3
    # 信号量，同时只允许3个线程运行
    threading.BoundedSemaphore(threadnum)
    # 默认3线程现在，也可以通过传参的方式设置线程数
    step = filesize // threadnum
    mtd_list = []
    start = 0
    end = -1

    if os.path.exists(filename):
        pass
    else:
        # 请空并生成文件
        tempf = open(filename, 'w')
        tempf.close()
        # rb+ ，二进制打开，可任意位置读写
        with open(filename, 'rb+') as f:
            fileno = f.fileno()
            # 如果文件大小为11字节，那就是获取文件0-10的位置的数据。如果end = 10，说明数据已经获取完了。
            while end < filesize - 1:
                start = end + 1
                end = start + step - 1
                if end > filesize:
                    end = filesize
                # print("start:%s, end:%s"%(start,end))
                # 复制文件句柄
                dup = os.dup(fileno)
                # print(dup)
                # 打开文件
                fd = os.fdopen(dup, 'rb+', -1)
                # print(fd)
                t = MulThreadDownload(url, start, end, fd)
                t.start()
                mtd_list.append(t)

            for i in mtd_list:
                i.join()

if __name__ == "__main__":
  category = sys.argv[1]
  page = sys.argv[2]
  limit = sys.argv[3]
  # print(category,page,limit) 
  bookCategoryInfo = getBookCategoryInfo(category,page,limit)
  print("Category %s count is: %s" % (category,bookCategoryInfo["otherResult"]["count"]))
  bookList = bookCategoryInfo['module']
  for bookInfo in bookList:
      if isCmpebooks(bookInfo['img']):
          pdfUrl = genPDFUrl(bookInfo['img'])
          pdfName = bookInfo['name']+".pdf"
          print('Download:', pdfName)
          downloadPdf(pdfName, pdfUrl)