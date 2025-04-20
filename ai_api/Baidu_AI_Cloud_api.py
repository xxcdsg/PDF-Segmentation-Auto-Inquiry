import requests
import json

import urllib3
from numpy.f2py.auxfuncs import throw_error
from openai import api_key

from config.config import *

def get_access_token():
    # 替换为你的API Key和Secret Key
    configs = load_configs()
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + configs['Baidu_api_key'] + "&client_secret=" + configs['Baidu_Secret_key']

    #尝试连接
    ptop = 0
    ok = False
    response = None
    while ptop < 5 and ok == False:
        try:
            response = requests.get(url)
            ok = True
        except requests.exceptions.RequestException as e:
            ptop += 1
            print(f"Error occurred: {e}")

    response_data = response.json()
    return response_data.get("access_token")

def send_question(access_token,messages,model_type = "ernie-speed-128k"):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/" + model_type + "?access_token=" + access_token
    payload = json.dumps({
        "messages": messages,
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
    ptop = 0
    ok = False
    response = None
    while ptop < 5 and not ok:
        try:
            response = requests.post(url, headers=headers, data=payload)
            ok = True
        except :
            ptop += 1
            print("失败次数",ptop)

    return response.json()