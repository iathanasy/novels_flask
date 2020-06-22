from operator import itemgetter

from urllib.parse import urlparse
from novels.fetch_page import novels_chapter, novels_content, do_search
from flask import Flask, render_template, request, redirect, jsonify
from novels.rules import RULES


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/search', methods=["GET"])
def search():

    name = str(request.args.get('wd', '')).strip()
    if not name:
        return render_template('/')

    result = do_search(name)
    new_result = result[1]
    # 排序
    result_sorted = sorted(
        new_result,
        reverse=True,
        key=itemgetter('is_parse'))

    novels_name = name
    time = result[0]
    res = result_sorted
    count = len(result_sorted)
    return render_template('result.html',
                           novels_name=novels_name,
                           result=res,
                           time=time,
                           count=count)


"""
返回小说章节目录页
: content_url   这决定当前U页面url的生成方式
: url           章节目录页源url
: novels_name   小说名称
:return: 小说章节内容页
"""


@app.route('/chapter')
def chapter():
    url = request.args.get('url', None)
    novels_name = request.args.get('novels_name', None)
    netloc = urlparse(url).netloc
    if netloc not in RULES.keys():
        return redirect(url)

    content_url = RULES[netloc].content_url
    # 章节抓取
    content = novels_chapter(url, netloc)
    if content:
        content = str(content).strip('[],, Jjs').replace(', ', '').replace('onerror', '').replace('js', '').replace(
            '加入书架', '')
        return render_template(
            'chapter.html',
            novels_name=novels_name,
            url=url,
            content_url=content_url,
            soup=content)
    else:
        return '解析失败，请将失败页面反馈给本站，请重新刷新一次，或者访问源网页：{url}'.format(url=url)


"""
返回小说章节内容页
: content_url   这决定当前U页面url的生成方式
: url           章节内容页源url
: chapter_url   小说目录源url
: novels_name   小说名称
:return: 小说章节内容页
"""


@app.route('/content')
def content():
    url = request.args.get('url', None)
    chapter_url = request.args.get('chapter_url', None)
    novels_name = request.args.get('novels_name', None)
    name = request.args.get('name', '')
    is_ajax = request.args.get('is_ajax', '')

    # 不在规则内 跳转源网页
    netloc = urlparse(url).netloc
    if netloc not in RULES.keys():
        return redirect(url)

    # 拼接小说目录url
    book_url = "/chapter?url={chapter_url}&novels_name={novels_name}".format(
        chapter_url=chapter_url,
        novels_name=novels_name)

    content_url = RULES[netloc].content_url
    content_data = novels_content(url, netloc)
    if content_data:
        try:
            content = content_data.get('content', '获取失败')
            next_chapter = content_data.get('next_chapter', [])
            title = content_data.get('title', '').replace(novels_name, '')
            name = title if title else name

            # 拼接小说书签url
            bookmark_url = "{path}?url={url}&name={name}&chapter_url={chapter_url}&novels_name={novels_name}".format(
                path=request.path,
                url=url,
                name=name,
                chapter_url=chapter_url,
                novels_name=novels_name
            )

            # 破坏广告链接
            content = str(content).strip('[]Jjs,').replace('http', 'hs').replace('.js', '').replace('();', '')

            # 返回json
            if is_ajax == "owl_cache":
                owl_cache_dict = dict(
                    name=name,
                    url=url,
                    content_url=content_url,
                    chapter_url=chapter_url,
                    novels_name=novels_name,
                    next_chapter=next_chapter,
                    soup=content
                )
                return jsonify(owl_cache_dict)

            return render_template(
                'content.html',
                name=name,
                url=url,
                content_url=content_url,
                chapter_url=chapter_url,
                novels_name=novels_name,
                next_chapter=next_chapter,
                soup=content)

        except Exception as e:
            print(e)
            return redirect(book_url)


'''
打包
进入项目 e:\novels\venv\Scripts cmd
输入 activate
返回项目根目录 cd .. cd ..
输入命令 pip freeze >requirements.txt

部署 pip install -r requirements.txt
启动 python app.py
'''
if __name__ == '__main__':
    app.run()
