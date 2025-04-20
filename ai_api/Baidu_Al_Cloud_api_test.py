import requests
import json

def get_access_token():
    # 替换为你的API Key和Secret Key
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=uXv0kEiuNZjrpesGDtmtCPKC&client_secret=QIgMR224LfW4nLijQ3dRQiIiU7MsTTTr"
    response = requests.get(url)
    response_data = response.json()
    return response_data.get("access_token")


def send_question(user_input, access_token, context=None):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + access_token
    # 注意：上面的URL中的your_service_endpoint需要替换为您实际使用的服务端点

    # 构建请求负载，现在包含用户的实际输入
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "你好"
            },
            {
                "role": "assistant",
                "content": "你好"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        # 注意：以下参数可能需要根据您的实际服务进行调整
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


# 主函数，处理多轮对话
def main():
    access_token = get_access_token()
    context = None  # 用于存储对话上下文的变量（如果需要）
    print("开始连续问答，输入'exit'退出。")
    while True:
        user_input = input("请输入您的问题（或输入'exit'退出）：")
        if user_input.lower() == 'exit':
            print("退出连续问答。")
            break
        response_data = send_question(user_input, access_token, context)
        # 根据您的服务响应格式，提取AI的回复

        if 'result' in response_data:
            print("AI回复：", response_data['result'])
            # context = response_data['content']
        else:
            print("没有返回结果或结果格式不正确。")

        # ai_reply = response_data.get("result", {}).get("answers", [{}])[0].get("content", "AI没有回复。")
        # print("AI回复：", ai_reply)

        # 更新上下文（如果需要）
        # context = update_context_based_on_response(response_data)

        # 检查是否需要重新获取access_token（根据您的token有效期来决定）
        # 如果需要，可以在这里重新获取access_token


if __name__ == '__main__':
    main()