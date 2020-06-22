import re
from operator import itemgetter
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from novels.config import headers
from novels.rules import RULES,LATEST_RULES

'''
百度搜索
'''
def baidu_so(novels_name):

    url = 'http://www.baidu.com/s'
    timeout = 10
    # novels_name = 'intitle:{name} 小说 阅读'.format(name=novels_name)
    novels_name = novels_name.strip()
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



