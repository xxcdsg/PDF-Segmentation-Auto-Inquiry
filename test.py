import re
import json
import pandas as pd
from pathlib import Path


def validate_and_convert(input_file='output.txt', output_file='汉字解析.xlsx'):
    """
    带校验功能的文本转Excel工具

    参数:
        input_file (str): 输入文本文件路径
        output_file (str): 输出Excel文件路径
    """
    try:
        # 读取文本内容
        text_content = Path(input_file).read_text(encoding='utf-8')

        # 匹配 "汉字标签: ```json...```" 的模式
        pattern = r'(\w+):\s*```json\n([\s\S]*?)\n```'
        matches = re.findall(pattern, text_content)

        if not matches:
            print("未检测到有效数据块")
            return False

        error_log = []
        all_data = []

        for label, json_block in matches:
            try:
                # 清洗并解析JSON
                cleaned = re.sub(r'[\x00-\x1F\x7F]', '', json_block)
                data = json.loads(cleaned)

                # 校验汉字字段
                for item in data:
                    if '汉字' not in item:
                        error_log.append(f"标签【{label}】的JSON缺少'汉字'字段")
                        continue

                    if item['汉字'] != label:
                        error_log.append(
                            f"数据不匹配！标签声明为【{label}】"
                            f"，但数据中的汉字字段为【{item['汉字']}】"
                        )

                all_data.extend(data)

            except json.JSONDecodeError as e:
                error_log.append(f"标签【{label}】的JSON解析失败：{str(e)}")
                continue

        # 输出错误日志
        if error_log:
            print("发现以下数据问题：")
            for i, error in enumerate(error_log, 1):
                print(f"{i}. {error}")

            if not all_data:
                print("所有数据校验未通过，终止转换")
                return False

            confirm = input("存在数据问题，是否继续转换？(y/n): ")
            if confirm.lower() != 'y':
                return False

        # 生成Excel文件
        df = pd.DataFrame(all_data)

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='校验数据')

            # 自动列宽调整
            worksheet = writer.sheets['校验数据']
            for col in worksheet.columns:
                max_len = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        cell_len = len(str(cell.value))
                        max_len = max(max_len, cell_len)
                    except:
                        pass
                worksheet.column_dimensions[column].width = (max_len + 2) * 1.2

        print(f"生成文件成功：{output_file}")
        print(f"有效数据量：{len(all_data)}条")
        return True

    except FileNotFoundError:
        print(f"错误：输入文件 {input_file} 不存在")
    except Exception as e:
        print(f"运行时异常：{str(e)}")
    return False


if __name__ == "__main__":
    validate_and_convert()