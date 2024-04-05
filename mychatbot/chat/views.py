from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Conversation
# 引入情感分析和聊天机器人的API（等我们到这一步再填写）

def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('text')
        # 这里你可以调用聊天机器人API获取回复
        bot_response = '这里是机器人的回复'  # 模拟回复，后续将接入真实API

        # 创建会话记录
        Conversation.objects.create(user_input=user_input, bot_response=bot_response)

        # 结合情感分析的结果（这个是后续步骤）

        return JsonResponse({'response': bot_response})
        
    return JsonResponse({'error': 'Invalid request'}, status=400)