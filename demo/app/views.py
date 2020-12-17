from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jieba
# Create your views here.

# 初始化中文分词
token = lambda x:list(jieba.cut(x))

# 取消当前函数防跨站请求伪造功能，即便setting中设置了全局中间件
@csrf_exempt
# 定义处理request 的函数
def tokenizer(request):
    # 提取request中请求方式判断
    if request.method == 'POST':
        # 解析request的数据
        data = JSONParser().parse(request)
        # 获取key 为text 的value
        text = data.get('text')
        # 调用前面初始化的分词函数来处理 requests
        result = token(text)
        # 返回（response）分词结果给用户
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse("Error", safe=False)
