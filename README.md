# novels_flask

安装：

```
# 数据库驱动
pip install pymysql
# 数据库连接池
pip install DBUtils
```

## 建表

```
CREATE TABLE `novel` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `book_name` varchar(100) NOT NULL COMMENT '书名',
  `chapter_name` varchar(100) NOT NULL COMMENT '章节',
  `source` varchar(100) NOT NULL COMMENT '来源',
  `content` text NOT NULL COMMENT '内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```

## 运行
`fetch_page.py`