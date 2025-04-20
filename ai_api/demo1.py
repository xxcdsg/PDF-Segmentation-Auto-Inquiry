import requests
import json

def get_access_token():
    # 替换为你的API Key和Secret Key
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=uXv0kEiuNZjrpesGDtmtCPKC&client_secret=QIgMR224LfW4nLijQ3dRQiIiU7MsTTTr"
    response = requests.get(url)
    response_data = response.json()
    return response_data.get("access_token")

def send_question(user_input, access_token):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + access_token
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "stream": False,
        "temperature": 0.9,
        "top_p": 0.7,
        "penalty_score": 1,
        "system": "专业的地质找矿专家和金矿矿床学家",
        "max_output_tokens": 4096,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.0,
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

def main():
    access_token = get_access_token()
    print("开始连续问答，输入'exit'退出。")
    while True:
        user_input = input("请输入您的问题（或输入'exit'退出）：")
        if user_input.lower() == 'exit':
            print("退出连续问答。")
            break
        response_data = send_question(user_input, access_token)
        if 'result' in response_data:
            print("AI回复：", response_data['result'])
        else:
            print("没有返回结果或结果格式不正确。")
        # 检查是否需要重新获取access_token（根据token的有效期来决定）
        # 如果需要，可以在这里重新获取access_token
        # 例如，如果token有效期为1小时，可以在每次问答后检查时间，必要时重新获取

if __name__ == '__main__':
    main()