import falcon  # 导入falcon
import json  # 导入json处理模块
import jieba  # 导入分词器模块
from wsgiref import simple_server  # 导入wsgi(Web Server Gateway Interface )服务模块

#定义分词器处理函数
def token(x):
    return jieba.lcut(x)

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
            resp.body = json.dumps({"response": words})
        except exception as e:
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
