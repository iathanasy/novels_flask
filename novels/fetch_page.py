#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import re
import urllib.request,urllib.parse
from operator import itemgetter
from urllib.parse import urljoin,urlparse
import requests
from novels.config import headers

from bs4 import BeautifulSoup
from novels.rules import RULES
from novels.extract import extract_pre_next_chapter,extract_chapters
import sys
# 最大递归深度 默认999
sys.setrecursionlimit(9000000)  # 这里设置大一些


# 下载页面
def download(url):
    netloc = urlparse(url).netloc

    # 会出现 网站解码问题
    # req = urllib.request.Request(url=url, headers=headers, method="GET")
    # res = urllib.request.urlopen(req, timeout=10)
    # encoding = RULES[netloc].encoding
    # return res.read().decode(encoding)

    # requests
    res = requests.get(url, headers=headers, timeout=10)
    encoding = RULES[netloc].encoding
    return res.content.decode(encoding)


# 章节抓取
def novels_chapter(url, netloc):
    html = download(url)
    if html:
        soup = BeautifulSoup(html, 'html5lib')
        selector = RULES[netloc].chapter_selector
        if selector.get('id', None):
            content = soup.find_all(id=selector['id'])
        elif selector.get('class', None):
            content = soup.find_all(class_=selector['class'])
        else:
            content = soup.find_all(selector.get('tag'))
        # 防止章节被display:none
        return str(content).replace('style', '') if content else None
    return None

# 内容抓取
def novels_content(url, netloc):
    html = download(url)
    if html:
        # soup = BeautifulSoup(html, 'html5lib')
        soup = BeautifulSoup(html, 'html.parser')
        selector = RULES[netloc].content_selector
        if selector.get('id', None):
            content = soup.find_all(id=selector['id'])
        elif selector.get('class', None):
            content = soup.find_all(class_=selector['class'])
        else:
            content = soup.find_all(selector.get('tag'))

        if content:
            # 提取出真正的章节标题
            title_reg = r'(第?\s*[一二两三四五六七八九十○零百千万亿0-9１２３４５６７８９０]{1,6}\s*[章回卷节折篇幕集]\s*.*?)[_,-]'
            title = soup.title.string
            extract_title = re.findall(title_reg, title, re.I)
            if extract_title:
                title = extract_title[0]
            else:
                title = soup.select('h1')[0].get_text()
            if not title:
                title = soup.title.string
            # if "_" in title:
            #     title = title.split('_')[0]
            # elif "-" in title:
            #     title = title.split('-')[0]
            next_chapter = extract_pre_next_chapter(chapter_url=url, html=str(soup))
            #text 去掉html标签
            # content = [str(i.text) for i in content]

            data = {
                # 'content': str(''.join(content)),
                'content': content,
                'next_chapter': next_chapter,
                'title': title
            }
        else:
            data = None
        return data
    return None


# 递归获取
def content_f(book_name,url):
    netloc = urlparse(url).netloc
    content = novels_content(url, netloc)
    # 处理最后一章
    if not content: return

    title = content.get('title')
    content_txt = content.get('content').strip().split('\xa0'*4)
    print(title, url)
    # 存储
    content_write(book_name, title, content_txt)
    # 获取下一章
    if content.get('next_chapter', None):
        # for k,v in content['next_chapter'].items():
        #     print(k,v)
        next_url = content['next_chapter'].get('下一章')
        if url != next_url:
            content_f(book_name, next_url)

# 内容存储
def content_write(book_name, chapter_name, content):
    with open(book_name, 'a', encoding='utf-8') as f:
        f.write(chapter_name)
        f.write('\n')
        f.write('\n'.join(content))
        f.write('\n')


if __name__ == '__main__':

    # url = 'https://www.baidu.com/link?url=ofN4BS4oAvfnnz5Ud6eqe3NdmUevTcrqre1ezMj5pG5nQ53PmhIDNTYnuTLSPFpFSi_j4iYe1ROR2k-NL8aIra&wd=&eqid=ffd10bc60000701a000000065ee43fde'
    # print(get_real_url(url))

    # 提取 baseurl
    # url = 'https://blog.csdn.net/u012249992/article/details/79525396'
    # netloc = urlparse(url).netloc
    # print(netloc)

    # 章节抓取
    # url = "https://www.biqukan.com/38_38836/"
    # url = "https://www.booktxt.net/1_1562/"
    # url = "http://www.biquge.info/22_22533/"
    url = "https://www.23txt.com/files/article/html/37/37532/"
    netloc = urlparse(url).netloc
    chapter_html = novels_chapter(url, netloc)
    chapters = extract_chapters(url, chapter_html)
    print(chapters)

    #
    # chapters = []
    # bs = BeautifulSoup(chapter_html, 'html.parser')
    # for link in bs.find_all('a'):
    #     data = {}
    #     url = urljoin(url, link.get('href')) or ''
    #     name = link.text
    #     data['chapters_url'] = url
    #     data['chapters_name'] = name
    #     data['index'] = int(urlparse(url).path.split('.')[0].split('/')[-1])
    #     chapters.append(data)
    # #排序
    # chapters_sorted = sorted(chapters, reverse=True, key=itemgetter('index'))
    # print(chapters_sorted)


    # 内容抓取
    # book_name = "沧元图.txt"
    # url = 'https://www.biqukan.com/38_38836/497783246.html'
    # content_f(book_name, url)

    # book_name = '凡人修仙传.txt'
    # url = 'https://www.xsbiquge.com/1_1366/8673848.html'
    # # https://www.xsbiquge.com/1_1366/8674818.html
    # content_f(book_name, url)

    # html = download('https://www.biqukan.com/38_38836/542434096.html')
    # print(html)

    '''
    baseurl = 'https://www.biqukan.com/'
    # pattern = re.compile('href="[^(javascript)]\S*[^(#)(css)(js)(ico)]\"')
    pattern = re.compile('<a href="(.*?)" (.*?)>(.*?)</a>')
    url_pattern = re.compile('/\d{1,5}_\d{1,10}/')
    html = download(baseurl)
    #print(html)
    arr = re.findall(pattern, html)

    i = 1
    for u in arr:
        url_re = re.findall(url_pattern, u[0])
        title = u[2]
        if len(url_re) == 1 and title.find('<img') == -1:
            url = urllib.parse.urljoin(baseurl, url_re[0])
            print((i,url,title))
            i += 1
    '''
