import requests

# 替换为你实际的 API token（确保没有非 ASCII 字符）
api_token = '9bc7d121-cde4-4437-aa3a-d0d16786a18e'

# API 请求的地址
api_url = 'https://keyue.cloud.baidu.com/online/core/v5/stream/query'

# 请求的头部，确保 token 和 Content-Type 没有非 ASCII 字符
headers = {
    'token': api_token.encode('ascii', 'ignore').decode('ascii'),
    'Content-Type': 'application/json'
}

# 要发送到 API 的数据，没有非 ASCII 字符
data = {
    "queryText": "你好",
    "sessionId": "ecb95fcc-0e49-4ab0-b026-c20a8aac1585"
}

try:
    # 使用 POST 方法发送请求
    response = requests.post(api_url, headers=headers, json=data)
    response.encoding = 'utf-8'  # 添加这行代码

    # 输出响应内容
    print(response.text)
except UnicodeEncodeError as e:
    print('Encoding Error:', e)