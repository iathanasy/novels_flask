#!/usr/bin/env python3
# -*-coding:utf-8 -*-

'''
360搜索搜索
'''
import re
import time
from operator import itemgetter
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

from novels.function import get_random_user_agent
from novels.rules import RULES, LATEST_RULES


def so_so(novels_name):
    url = 'https://www.so.com/s'
    timeout = 10

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'User-Agent': get_random_user_agent(),
        'Referer': "http://www.so.com/haosou.html?src=home"
    }

    novels_name = "{name} 小说 最新章节".format(name=novels_name)
    params = {'ie': 'utf-8', 'src': 'noscript_home', 'shb': 1, 'q': novels_name}

    resp = requests.get(url, headers=headers, params=params, timeout=timeout)
    html = resp.content.decode()
    soup = BeautifulSoup(html, 'html5lib')

    parse_result = []
    result = soup.find_all(class_='res-list')
    for res in result:
        try:
            url = res.select('h3 a')[0].get('href', None)
            title = res.select('h3 a')[0].get_text()
        except:
            url, title = None, None
            print('error')

        if not url:
            continue
        # 针对不同的请进行url的提取
        if "www.so.com/link?m=" in url:
            url = res.select('h3 a')[0].get('data-mdurl', None)
        if "www.so.com/link?url=" in url:
            url = parse_qs(urlparse(url).query).get('url', None)
            url = url[0] if url else None


        real_str_url = str(url)
        netloc = urlparse(real_str_url).netloc
        # 是否解析
        is_parse = 1 if netloc in RULES.keys() else 0
        # 是否在规则内
        is_rules = 1 if netloc in LATEST_RULES else 0
        if is_rules:
            ree = {'title':title, 'netloc': netloc, 'url': url, 'is_parse': is_parse}
            parse_result.append(ree)

    # 排序
    # result_sorted = sorted(
    #     parse_result,
    #     reverse=True,
    #     key=itemgetter('is_parse'))


    return parse_result


if __name__ == '__main__':
    print(so_so('凡人'))

