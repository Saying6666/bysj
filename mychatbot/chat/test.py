import requests
import json

# token卡直接替换key为你的key
OPENAI_API_KEY = 'sk-VKm5OwuNNepyGbc9607865734b514e2dA4Bd2dFbDaA5230d'
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

data = {'model': 'gpt-4', 'messages': [{'role': 'user', 'content': '鲁迅为什么暴打周树人'}],'stream':True}

# 次数卡直接替换接口为你的卡密
response = requests.post('https://api.zhtec.xyz/test/yQvEJRbpen.php', headers=headers, data=json.dumps(data), stream=True)

for chunk in response.iter_lines():
    if chunk:
        decoded_chunk = chunk.decode('utf-8')
        if decoded_chunk.startswith('data:'):
            # Remove the 'data: ' prefix and parse the JSON object
            try:
                parsed_chunk = json.loads(decoded_chunk[5:])
                print(parsed_chunk['choices'][0]['delta']['content'], end='')
            except:
                pass