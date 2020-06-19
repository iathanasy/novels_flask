import re
from operator import itemgetter
from urllib.parse import urlparse
import time
import requests
from bs4 import BeautifulSoup
from novels.config import headers
from novels.rules import RULES

'''
百度搜索
'''
def baidu_so(novels_name):
    start = time.time()
    url = 'http://www.baidu.com/s'
    timeout = 10
    novels_name = 'intitle:{name} 小说 阅读'.format(name=novels_name)
    params = {
        'wd': novels_name,
        'rn': 15,
        'ie': 'utf-8',
        'vf_bl': 1
    }

    resp = requests.get(url, headers=headers, params=params, timeout=timeout)
    html = resp.content.decode()
    soup = BeautifulSoup(html, 'html5lib')

    parse_result = []
    result = soup.find_all(class_='result')
    for res in result:
        url = res.select('h3.t a')[0]['href']
        title = res.select('h3.t a')[0].get_text()
        try:
            # 真实url
            url = get_real_url(url)
            # print(url)
        except:
            print('error')

        real_str_url = str(url)
        netloc = urlparse(real_str_url).netloc
        # 是否解析
        is_parse = 1 if netloc in RULES.keys() else 0

        ree = {'title':title, 'netloc': netloc, 'url': url, 'is_parse': is_parse}
        parse_result.append(ree)

    name = novels_name
    so_time = '%.2f' % (time.time() - start)
    count = len(parse_result)
    # 排序
    result_sorted = sorted(
        parse_result,
        reverse=True,
        key=itemgetter('is_parse'))

    ress = {'name':name, 'so_time': so_time, 'res': result_sorted, 'count': count}
    return ress


'''
 获取百度真实url地址
'''
def get_real_url(url):
    # res = requests.get(url, timeout=2)
    # real_url = res.url
    # return real_url

    # allow_redirects 设置不允许跳转
    tmpPage = requests.get(url, allow_redirects=False)
    if tmpPage.status_code == 200:
        urlMatch = re.search(r'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S)
        real_url = urlMatch.group(1)
    elif tmpPage.status_code == 302:
        real_url = tmpPage.headers.get('Location')
    else:
        real_url = 'No URL found!!'
    return real_url

if __name__ == '__main__':
    print(baidu_so('凡人'))



