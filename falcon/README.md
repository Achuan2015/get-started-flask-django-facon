# AImodel2service

#使用Falcon搭建Rest API
## 写在前面
本文档描述了用Falcon搭建一个简单的Rest API服务的过程

## Falcon简介
[Falcon](https://falcon.readthedocs.io/en/stable/user/intro.html)在官网中介绍自己是一个python的web API微服务框架(Falcon is a bare-metal Python web API framework for building high-performance microservices, app backends, and higher-level frameworks.)

**主要的优点：**（[参考github页面](https://github.com/falconry/falcon))

* Fast.
* Reliable.
* Flexible.
* Debuggable.


## 案例说明
为了简要说明问题，下面例子将会演示将中文分词功能制作成RestAPI变成web服务的全部过程；

## 依赖环境
需要Python-3.6环境 (推荐安装[Anaconda](https://anaconda.org/))

```bash
pip install jieba #(0.39)
pip install falcon
```

## 创建hello.py
```python
#hello.py
import falcon #导入falcon
import json  #导入json处理模块
import jieba #导入分词器模块
from wsgiref import simple_server #导入wsgi(Web Server Gateway Interface )服务模块

token = lambda x:list(jieba.cut(x)) #定义分词器处理函数

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class Resource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('\nYour api service is working.\n\n')

    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            raw_json = json.loads(req.stream.read())
            words = token(raw_json['text'])
            resp.body =  json.dumps({"response": words})
        except:
            #处理异常
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({"response": "value error"})

# 初始化falcon.API
app = falcon.API()

# 定义路由， 使/token路径的访问被处理
app.add_route('/token', Resource())

if __name__ == '__main__':
    #启动8000端口服务
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    print("Serving on port 8000...")
    httpd.serve_forever()

```


## 运行server
```bash
$ python hello.py
Serving on port 8000... #服务正常启动，等待连接

```

## 测试我们定义好的API
```bash
curl -i -H "Content-type: application/json" -X POST http://127.0.0.1:8000/token -d '
    {
        "text":"今天上海真的好冷啊！我也觉得啊！"
    }'

```
如果服务正常工作会得到如下返回：

```bash
{"response":["今天", "上海", "真的", "好", "冷", "啊", "！", "我", "也", "觉u5f97", "啊", "！"]}
```
如果传入的数据异常会得到如下返回：
```bash
{"response": "value error"}
```

