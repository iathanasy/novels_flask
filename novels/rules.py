#!/usr/bin/env python3
# -*-coding:utf-8 -*-

# tuple的升级版 namedtuple(具名元组)
from collections import namedtuple

'''
collections.namedtuple(typename, field_names, verbose=False, rename=False) 
    typename：元组名称
    field_names: 元组中元素的名称
    rename: 如果元素名称中含有 python 的关键字，则必须设置为 rename=True
    verbose: 默认就好
'''


# 两种方法来给 namedtuple 定义方法名
#Rules = namedtuple('Rules',['encoding','content_url','chapter_selector','content_selector'])
Rules = namedtuple('Rules','encoding content_url chapter_selector content_selector')

'''
各个网站的规则，仅限class和id,tag

encoding
    网站编码
    
content_url
    -1	不解析，跳转到原本网页
    0	表示章节网页需要当前页面url拼接
    1	表示章节链接使用本身自带的链接，不用拼接
    netloc	用域名进行拼接
    
chapter_selector
    解析章节目录的规则
    
content_selector
    解析目录内容的规则

# 使用域名进行拼接
rules = Rules("https://www.biqukan.com/",{'class':'listmain'}, {'id':'content'}) 
'''


RULES ={
    "www.biqukan.com": Rules("gbk","https://www.biqukan.com/",{'class':'listmain'}, {'id':'content'}),
    "www.biquge.info": Rules("utf-8","0",{'id':'list'}, {'id':'content'}),
    "www.booktxt.net": Rules("gbk",'0',{'id':'list'}, {'id':'content'}),
    "www.23txt.com": Rules("gbk",'https://www.23txt.com/',{'id':'list'}, {'id':'content'}),
    'www.gdbzkz.com': Rules('utf-8','http://www.gdbzkz.com/', {'class': 'listmain'}, {'id': 'content'}),
    'www.quanben.net': Rules('utf-8','http://www.quanben.net/', {'class': 'chapterlist'}, {'id': 'BookText'}),
    "www.xsbiquge.com": Rules("utf-8","https://www.xsbiquge.com",{'id':'list'},{'id':'content'})
}


'''
最新规则， 只有这里面的网站才返回给页面
'''
LATEST_RULES = ['www.biqukan.com',
                'www.biquge.info',
                'www.booktxt.net',
                'www.23txt.com',
                'www.gdbzkz.com',
                'www.quanben.net',
                'www.xsbiquge.com',

                'www.biqugex.com',
                'www.x23us.com',
                'www.23us.la',
                'www.sqsxs.com',
                'www.nuomi9.com',
                'www.biquge.info',
                'www.biquge.tw',
                'www.qu.la',
                'www.shuquge.com',
                'www.jingcaiyuedu.com',
                'www.xshuyaya.com',
                ''
                ]



# 搜索引擎检索优先级
ENGINE_PRIORITY = ['360', 'baidu', 'bing']