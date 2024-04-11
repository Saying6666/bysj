import json
import re
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
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
    


from django.http import JsonResponse
import requests
import json


OPENAI_API_KEY = 'sk-VKm5OwuNNepyGbc9607865734b514e2dA4Bd2dFbDaA5230d'
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
@csrf_exempt
def chat_with_gpt(request):
    # 从POST请求中获取用户消息
    user_message = json.loads(request.body).get('message', '')
    #将user_message转化成字符串
    user_message = str(user_message)

    selected_model = json.loads(request.body).get('selectedModel', 'gpt-3.5-turbo-16k')
    print(f"User message: {user_message}")
    print(f"Selected model: {selected_model}")

    # 构造发送给GPT的消息，包括用户的消息
    prompt = "我希望你扮演一个情感分析大师。当我给你提供一段对话时，请分析并识别对话中用户的最新的情绪状态。我需要你直接回复包含的情绪，如快乐、悲伤、愤怒、惊讶、厌恶或恐惧等，不需要给出其他任何回复或建议。请确保分析结果遵循一致的格式输出。请注意，如果不包含情感，这可以输出没有检查到用户情感。我不希望看到有除了我的要求以外的其他回答"

    data = {
        'model': selected_model,
        'messages': [{'role': 'user', 'content': 'prompt: ' + prompt + '\n' + user_message}],
    }

    # 向OpenAI的API发送请求来分析情绪
    response = requests.post('https://api.zhtec.xyz/test/yQvEJRbpen.php', headers=headers, data=json.dumps(data))

    # 确保API请求成功
    if response.status_code == 200:
        complete_response_text = ""
        try:
            for chunk in response.iter_lines():
                if chunk:
                    decoded_chunk = chunk.decode('utf-8')
                    # 处理每一个流式JSON块
                    chunk_match = re.search(r'^data: (.+)', decoded_chunk)
                    if chunk_match:
                        json_data = chunk_match.group(1)
                        try:
                            response_json = json.loads(json_data)
                            text_chunk = response_json['choices'][0].get('delta', {}).get('content', "")
                            complete_response_text += text_chunk
                            if 'stop' in response_json['choices'][0]['delta'].get('finish_reason', ''):
                                break
                        except json.JSONDecodeError:
                            continue
            print("使用模型为：", selected_model)
            print(f"Complete response text: {complete_response_text}")
            return JsonResponse({"response": complete_response_text})
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("Error", status=500)
    else:
        print(f'GPT API request failed with status {response.status_code}')
        return HttpResponse("GPT API request failed", status=500)
