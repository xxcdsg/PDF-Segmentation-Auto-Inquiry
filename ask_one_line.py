from ai_api.glm_ai_api import send_question_glm
from ai_api.kimi_ai_api import send_message
from ai_api.messages_handle import *
from ai_api.Baidu_AI_Cloud_api import *
from ai_api.openai_api import send_question_open_ai
from ai_api.tx_deepseek_api import send_question_tx_deepseek
from config.hash_map import check_hash_map, load_in_hash_map

configs = load_configs()

ask_info = configs["ask_info"]

pre_prompt = configs["pre_prompt"]

# 总的来说，都是问一个模型，一段话，然后返回

def ask_one_line_tx_deepseek(user_input):
    if configs["hash_num"] == 1:
        res = check_hash_map(user_input)
        if res != "not exist":
            print("部分中存在")
            return res
    completion = send_question_tx_deepseek(build_messages(pre_prompt + " 段落原文:" + user_input))

    if 'No' in completion.choices[0].message.content:
        print("该行与提示词无关,跳过")
        return ""

    for idx in range(0, configs["ask_info_num"]):
        info = ask_info[idx]
        if idx == 0:
            info += "\n原文为：" + '\n' + user_input
            messages = build_messages(info)
        else:
            messages = []
            messages = extend_messages(info, output, messages)
        completion = send_question_tx_deepseek(messages)
        output = completion.choices[0].message.content
        # 输出中途结果
        if configs["print_info"] == 1:
            print(output)

    # 备份
    if configs["hash_num"] == 1:
        load_in_hash_map(user_input,output)

    return output

def ask_one_line_tx_deepseek_mul(user_input):
    completion = send_question_tx_deepseek(build_messages(pre_prompt + " 段落原文:" + user_input))

    if 'No' in completion.choices[0].message.content:
        print("该行与提示词无关,跳过")
        return [""]

    res = []

    for idx in range(0, configs["ask_info_num"]):
        info = ask_info[idx]
        if idx == 0:
            info += "\n原文为：" + '\n' + user_input
            messages = build_messages(info)
        else:
            messages = []
            messages = extend_messages(info, output, messages)
        completion = send_question_tx_deepseek(messages)
        output = completion.choices[0].message.content

        res.append(output)

        # 输出中途结果
        if configs["print_info"] == 1:
            print(output)

    return res

def ask_one_line_glm(user_input):
    output = ""

    # 检测备份中是否存在
    if configs["hash_num"] == 1:
        res = check_hash_map(user_input)
        if res != "not exist":
            print("部分中存在")
            return res

    completion = send_question_glm(build_messages(pre_prompt + " 段落原文:" + user_input))

    if 'No' in completion.choices[0].message.content:
        print("该行与金矿找矿无关,跳过")
        return ""

    for idx in range(0, configs["ask_info_num"]):
        info = ask_info[idx]
        if idx == 0:
            info += "\n原文为：" + '\n' + user_input
            messages = build_messages(info)
        else:
            messages = []
            messages = extend_messages(info, output, messages)
        completion = send_question_glm(messages)
        output = completion.choices[0].message.content
        # 输出中途结果
        if configs["print_info"] == 1:
            print(output)

    # 备份
    if configs["hash_num"] == 1:
        load_in_hash_map(user_input,output)

    return output


def ask_one_line_glm_mul(user_input):
    output = ""
    res = []

    completion = send_question_glm(build_messages(pre_prompt + " 段落原文:" + user_input))

    if 'No' in completion.choices[0].message.content:
        print("该行与金矿找矿无关,跳过")
        return [""]

    for idx in range(0, configs["ask_info_num"]):
        info = ask_info[idx]
        if idx == 0:
            info += "\n原文为：" + '\n' + user_input
            messages = build_messages(info)
        else:
            messages = []
            messages = extend_messages(info, output, messages)
            # messages = build_messages(info + '\n' + output)

        completion = send_question_glm(messages)
        output = completion.choices[0].message.content
        # 输出中途结果
        if configs["print_info"] == 1:
            print(output)
        res.append(output)

    return res

def ask_one_line_kimi(user_input):
    # 检测备份中是否存在
    if configs["hash_num"] == 1:
        res = check_hash_map(user_input)
        if res != "not exist":
            print("部分中存在")
            return res

    output = ""
    completion = send_message(build_messages(pre_prompt + " 段落原文:" + user_input))
    if 'No' in completion.choices[0].message.content:
        print("该行与金矿找矿无关,跳过")
        return ""

    for idx in range(0,configs["ask_info_num"]):
        info = ask_info[idx]
        if idx == 0:
            info += "\n原文为：" + '\n' + user_input
            messages = build_messages(info)
        else :
            # messages = []
            messages = extend_messages(info,output,messages)
        completion = send_message(messages)
        output = completion.choices[0].message.content
        if configs["print_info"] == 1:
            print(output)

    if configs["hash_num"] == 1:
        load_in_hash_map(user_input,output)

    return output

def ask_one_line_kimi_mul(user_input):

    output = ""
    completion = send_message(build_messages(pre_prompt + " 段落原文:" + user_input))
    if 'No' in completion.choices[0].message.content:
        print("该行与金矿找矿无关,跳过")
        return [""]

    res = []

    for idx in range(0, configs["ask_info_num"]):
        info = ask_info[idx]
        if idx == 0:
            info += "\n原文为：" + '\n' + user_input
            messages = build_messages(info)
        else:
            messages = extend_messages(info, output, messages)
        completion = send_message(messages)
        output = completion.choices[0].message.content
        if configs["print_info"] == 1:
            print(output)
        res.append(output)

    return res

def ask_one_line_baidu(user_input):
    # 检测备份中是否存在
    if configs["hash_num"] == 1:
        res = check_hash_map(user_input)
        if res != "not exist":
            print("部分中存在")
            return res

    messages = []
    output = ""
    access_token = get_access_token()

    #先判断该段是否有用
    pre_result = send_question(access_token, build_messages(pre_prompt + " 段落原文:" + user_input))
    if 'No' in pre_result['result'] :
        print("该行与金矿找矿无关,跳过")
        return ""

    for idx in range(0,configs["ask_info_num"]):
        info = ask_info[idx]
        if idx == 0:
            info += "\n原文为：" + '\n' + user_input
            messages = build_messages(info)
        else :
            messages = extend_messages(info,output,messages)
        print(info)
        response_data = send_question(access_token,messages)
        if 'result' in response_data:
            output = response_data['result']
            if configs["print_info"] == 1:
                print(output)
        else:
            print("没有返回结果或结果格式不正确。")

    if configs["hash_num"] == 1:
        load_in_hash_map(user_input,output)

    return output

def ask_one_line_baidu_mul(user_input):

    messages = []
    output = ""
    access_token = get_access_token()

    res = []

    #先判断该段是否有用
    pre_result = send_question(access_token, build_messages(pre_prompt + " 段落原文:" + user_input))
    if 'No' in pre_result['result'] :
        print("该行与金矿找矿无关,跳过")
        return [""]

    for idx in range(0,configs["ask_info_num"]):
        info = ask_info[idx]
        if idx == 0:
            info += "\n原文为：" + '\n' + user_input
            messages = build_messages(info)
        else :
            messages = extend_messages(info,output,messages)
        response_data = send_question(access_token,messages)
        if 'result' in response_data:
            output = response_data['result']
            if configs["print_info"] == 1:
                print(output)
            res.append(output)
        else:
            print("没有返回结果或结果格式不正确。")

    return res

def ask_one_line_openai_mul(user_input,api_key,base_url,model):
    completion = send_question_open_ai(build_messages(pre_prompt + " 段落原文:" + user_input),api_key,base_url,model)

    if 'No' in completion.choices[0].message.content:
        print("该行与提示词无关,跳过")
        return [""]

    res = []

    for idx in range(0, configs["ask_info_num"]):
        info = ask_info[idx]
        if idx == 0:
            info += "\n原文为：" + '\n' + user_input
            messages = build_messages(info)
        else:
            messages = []
            messages = extend_messages(info, output, messages)
        completion = send_question_tx_deepseek(messages)
        output = completion.choices[0].message.content

        res.append(output)

        # 输出中途结果
        if configs["print_info"] == 1:
            print(output)

    return res

def ask_one_line(user_input):

    model_type = configs["model_type"]

    if model_type == "kimi":
        return ask_one_line_kimi(user_input)
    if model_type == "baidu":
        return ask_one_line_baidu(user_input)
    if model_type == "glm":
        return ask_one_line_glm(user_input)
    if model_type == "tx_deepseek":
        return ask_one_line_tx_deepseek(user_input)

def ask_one_line_mul(user_input):
    model_type = configs["model_type"]

    if model_type == "kimi":
        return ask_one_line_kimi_mul(user_input)
    if model_type == "baidu":
        return ask_one_line_baidu_mul(user_input)
    if model_type == "glm":
        return ask_one_line_glm_mul(user_input)
    if model_type == "tx_deepseek":
        return ask_one_line_tx_deepseek_mul(user_input)
    if model_type == "openai_mod":
        _key = configs["openai_api_key"]
        _url = configs["openai_baseurl"]
        _model = configs["openai_model"]
        return ask_one_line_openai_mul(user_input,_key,_url,_model)