import os
from config.config import load_configs

configs = load_configs()

# 获取源文件所在的目录
def get_source_file_dir():
    source_file_path = os.path.abspath(__file__)
    return os.path.dirname(source_file_path)

def extract_text_between_pipes(input_string):
    # 找到第一个'|'的位置
    first_pipe_index = input_string.find('|')
    if first_pipe_index == -1:
        # 如果没有找到'|'，则返回空字符串
        return ""

    # 找到最后一个'|'的位置
    last_pipe_index = input_string.rfind('|')
    if last_pipe_index == -1 or last_pipe_index <= first_pipe_index:
        # 如果没有找到最后一个'|'，或者最后一个'|'在第一个'|'之前（或相同位置），则返回空字符串
        return ""

    # 提取两个'|'之间的文字
    extracted_text = input_string[first_pipe_index:last_pipe_index + 1]
    return extracted_text

def delete_the_first_two_lines(input_string):
    # 将字符串按行分割成列表
    lines = input_string.split('\n')

    # 如果字符串的行数小于等于2，则返回空字符串
    if len(lines) <= 2:
        return ""

    # 去除前两行
    lines = lines[2:]

    # 将剩余的行重新拼接成字符串
    result = '\n'.join(lines)
    return result


def save_string_to_markdown(file_name, input_string):
    file_path = get_source_file_dir() + "\\" + file_name + '.md'
    # 以写入模式打开文件，如果文件不存在则创建它
    with open(file_path, 'w', encoding='utf-8') as file:
        # 将字符串写入文件
        file.write(input_string)

def list_to_string(input_list):
    is_first_item = True
    result = ""
    for _item in input_list:
        item = _item

        # 取最后一个
        if configs["output_info"]:
            if len(_item) == configs["ask_info_num"]:
                item = _item[configs["ask_info_num"] - 1]
            else :
                item = ""

        item = extract_text_between_pipes(item)
        if is_first_item and len(item) > 0:
            is_first_item = False
        else:
            item = delete_the_first_two_lines(item)
        result += item
    return result

# 重定义下标
def reload_index(input_string):
    lines = input_string.split('\n')
    res = ""
    if len(lines) >= 2:
        res = lines[0] + '\n' + lines[1]
    ptop = 1
    for index in range(2,len(lines)):
        res += ("\n|" + str(ptop).rjust(10) + lines[index][7:])
        ptop += 1
    return res

def list_to_markdown(filename,input_list):
    # print(input_list)
    res = list_to_string(input_list)
    # print(res)
    res = reload_index(res)
    # print(res)
    lis = []
    lis.append(filename)
    save_string_to_markdown(filename, res)
    if configs["output_info"]:
        for index in range(0,configs["ask_info_num"]):
            ptop = 0
            res = ""
            for item in input_list:
                if item == [""]:
                    continue
                _item = item[index]
                res += f"\n-----{ptop}-----\n"
                ptop += 1
                res += _item

            save_string_to_markdown(filename + f"-{index}", res)
            lis.append(filename + f"-{index}")
    return lis # 返回文件合集
