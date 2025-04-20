import os
import json

def get_source_file_dir():
    source_file_path = os.path.abspath(__file__)
    return os.path.dirname(source_file_path)

hash_map_file_name = get_source_file_dir() + "\\hash_map.json"

def load_hash_map():
    try:
        with open(hash_map_file_name, 'r', encoding='utf-8') as f:
            dic = json.load(f)
    except FileNotFoundError:
        print("hash_map.json不存在")
        dic = []  # 如果文件不存在，则返回一个空列表
    except json.JSONDecodeError:
        print("hash_map.json不是有效的JSON文件")
        dic = []  # 如果文件内容不是有效的JSON，则返回一个空列表，并可能需要记录错误
    return dic

hash_map = load_hash_map()

def check_hash_map(s):
    if s in hash_map:
        return hash_map[s]
    else :
        return "not exist"

lis = []

def load_in_hash_map(_input,_output):
    lis.append((_input,_output))
    if len(lis) > 10:
        for (x,y) in lis:
            hash_map[x] = y
        lis.clear()
        with open(hash_map_file_name, 'w', encoding='utf-8') as f:
            json.dump(hash_map , f, ensure_ascii=False, indent=4)

def clear_hash_map():
    hash_map.clear()
    with open(hash_map_file_name, 'w', encoding='utf-8') as f:
        json.dump(hash_map, f, ensure_ascii=False, indent=4)