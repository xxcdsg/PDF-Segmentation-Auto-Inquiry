import json
import os
import sys

# config_file_name = 'C:/Users/Administrator/Desktop/code/python/pythonProject2/config/config.json'

config_defaults = [] # 默认参数种类

# 获取源文件所在的目录
def get_source_file_dir():
    source_file_path = os.path.abspath(__file__)
    return os.path.dirname(source_file_path)

config_file_name = get_source_file_dir() + "\\config.json"

# print(config_file_name)

def load_configs():
    try:
        with open(config_file_name, 'r', encoding='utf-8') as f:
            configs = json.load(f)
    except FileNotFoundError:
        print("config.json不存在")
        configs = []  # 如果文件不存在，则返回一个空列表
    except json.JSONDecodeError:
        print("config.json不是有效的JSON文件")
        configs = []  # 如果文件内容不是有效的JSON，则返回一个空列表，并可能需要记录错误
    return configs


def write_configs(configs_to_write):
    with open(config_file_name, 'w', encoding='utf-8') as f:
        json.dump(configs_to_write, f, ensure_ascii=False, indent=4)

def change_config(configs, key, value):
    for config in configs:
        if key in config:
            config[key] = value
            return configs  # 更新后直接返回
    # 如果键不存在于任何字典中，则添加一个新的字典
    configs.append({key: value})
    return configs

def init_configs(configs):
    for key in config_defaults :
        if key not in configs:
            configs.append({key : ''})
    return configs # 初始化空缺数据

def read_configs(key):
    configs = load_configs()
    if key not in configs:
        return None
    else :
        return configs[key]

# "Baidu_api_key": "uXv0kEiuNZjrpesGDtmtCPKC",
# "Baidu_Secret_key": "QIgMR224LfW4nLijQ3dRQiIiU7MsTTTr"

# configs = {
#     "Baidu_api_key": "uXv0kEiuNZjrpesGDtmtCPKC",
#     "Baidu_Secret_key": "QIgMR224LfW4nLijQ3dRQiIiU7MsTTTr"
# }
#
# write_configs(configs)
# print(load_configs())