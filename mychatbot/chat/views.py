import json
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import requests
from .models import Conversation
from django.views.decorators.csrf import csrf_exempt
# 引入情感分析和聊天机器人的API（等我们到这一步再填写）

# 主页视图
def index_view(request):
    return render(request, 'chat/chat.html')


# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

@csrf_exempt
def chat_with_baidu_unit(request):
    if request.method == 'POST':
        # 获取前端发送的数据
        body_unicode = request.body.decode('utf-8')# 解码请求体
        body = json.loads(body_unicode)# 解析请求体
        query_text = body.get('queryText')# 获取queryText
        session_id = body.get('sessionId', '')# 获取sessionId

        print(f'Backend received queryText: {query_text}')  # 打印查询文本
        if session_id:
            print(f'Backend received sessionId: {session_id}')  # 打印会话ID

        # 百度UNIT LLM接口信息
        api_url = "https://keyue.cloud.baidu.com/online/core/v5/block/query"
        api_key = '9bc7d121-cde4-4437-aa3a-d0d16786a18e'  # 替换为你的API Key

        headers = {
            'Content-Type': 'application/json',
            'token': api_key,
        }
        data = {
            "queryText": query_text,
            "sessionId": session_id
        }

        response = requests.post(api_url, headers=headers, json=data)# 发送POST请求
        print(f'Backend received response from UNIT LLM: {response.text}')  # 打印整个响应文本

        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            print(f'Error from UNIT LLM: {response.text}')  # 发生错误时打印错误信息
            return JsonResponse({'error': 'Communication with UNIT LLM failed'}, status=response.status_code)
    else:
        print('Backend received non-POST request')  # 打印非POST请求信息
        return JsonResponse({'error': 'Invalid request method. Only POST is supported.'}, status=400)