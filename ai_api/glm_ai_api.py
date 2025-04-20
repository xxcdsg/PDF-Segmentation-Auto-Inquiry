from zhipuai import ZhipuAI

from config.config import load_configs

def send_question_glm(messages):
    configs = load_configs()
    client = ZhipuAI(api_key=configs["Zhipu_api_key"])  # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4-long",  # 请填写您要调用的模型名称
        messages=messages,
    )
    return response
    # print(response.choices[0].message)
