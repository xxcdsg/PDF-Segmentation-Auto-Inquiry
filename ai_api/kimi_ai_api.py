# sk-VDfqLiHfeSFftiY0DVid4tGW8KAk04JLdwBxxNmYkr1edVjC
from grpc.framework.interfaces.base.utilities import completion
from openai import OpenAI

from config.config import load_configs

configs = load_configs()

client = OpenAI(
    api_key=configs["kimi_api_key"],
    base_url="https://api.moonshot.cn/v1",
)

def send_message(messages):

    ptop = 0
    ok = False
    completion = None
    while ptop < 5 and not ok:
        try:
            completion = client.chat.completions.create(
                model="moonshot-v1-128k",
                messages=messages,
                temperature=0.3,
            )
            ok = True
        except Exception as e:
            print("连接错误",e,"重试",ptop)
            ptop += 1

    return completion

    # print(completion.choices[0].message)