import re
import urllib.request as request
from bs4 import BeautifulSoup
import requests
import os
from concurrent.futures import  ThreadPoolExecutor


#章节TXT文件不存在，请检查！
'''''全局变量声明， 下载其它小说请注意修改 [下载到的本地目录, 书号, 起始index号]'''
downLoadFile = '/root/txt_cpxs/'  
err = '﻿  章节TXT文件不存在，请检查！'





'''''''自动产生新的url'''


def setNewUrl():
    urls = []
    for first in range(19, 20):
        for second in range(18001, 20912):
            for x in range(1305990, 1400000):
                xsr = 'http://www.******.com/'+ str(first) + '_' + str(second) +'/'+ str(x) +'.html'  #对应的单章html
                urls.append(xsr)
            return urls



def setTxts(urls):
    for url in urls:
        setDoc(setSrr(url))


def setSrr(url):
    print(url)
    if (requests.get(url).status_code == 404):
        print('这是个错误网址')
    if (requests.get(url).status_code == 500):
        print('服务器错误')
        return []
    print('正在打开 ', url)

    l = []
    '''''''请求响应和不响应的处理'''
    response = request.urlopen(url)

    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    err = str(soup)
    err =err.strip()
    if err == '﻿  章节TXT文件不存在，请检查！':
        l = err
        print (l)
        return l
    else:
        item = soup.findAll('span')
        title = str(item).split('>')[1]
        l.append(title.split('<')[0])
        strings = soup.findAll('div', id="chaptercontent")[0];
        for string in strings:
            st = string.__str__()
            if (len(st.split('<br/>')) > 1):
                pass
            else:
                l.append(st)
        setDoc(l)

# 穿入字符串 写入文件；标题为l[0]
def setDoc(l):
    if l == err:
        print(l)
    else:
        if (len(l) < 2):
            return
        if not os.path.exists(downLoadFile):
            os.makedirs(downLoadFile)
        file_s = downLoadFile + l[0] + '.txt'
        file = open(file_s, 'w+', encoding='utf-8')
        for i in l:
            file.write('\t')
            for ii in i.split('    '):
                file.write(ii)
            file.write('\n')


if __name__ == "__main__":

    print(  'ok'  )
    urls = setNewUrl()
    with ThreadPoolExecutor(max_workers=1000) as work:
        for url in urls:
            work.submit(setSrr, url)




