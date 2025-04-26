import requests
import json

import urllib3
from numpy.f2py.auxfuncs import throw_error
from openai import api_key, OpenAI

from config.config import *

def send_question_open_ai(messages,api_key,base_url,model):
    configs = load_configs()
    client = OpenAI(
        # 请用知识引擎原子能力API Key将下行替换为：api_key="sk-xxx",
        api_key=api_key,  # 如何获取API Key：https://cloud.tencent.com/document/product/1772/115970
        base_url=base_url,
    )
    completion = client.chat.completions.create(
        model=model,  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=messages,
    )
    return completion