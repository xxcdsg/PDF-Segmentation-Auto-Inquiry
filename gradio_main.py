import zipfile

import gradio as gr
import os
import pdf_to_markdown
from config.config import load_configs, write_configs
from data_processing.string_processing import list_to_markdown
from markdown_read import get_lines
from parallel.parallel_main import process_lines_parallel

# 获取源文件所在的目录
def get_source_file_dir():
    source_file_path = os.path.abspath(__file__)
    return os.path.dirname(source_file_path)


def generate_zip(files_to_zip):

    # 创建 ZIP 文件
    zip_path = "output.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file, os.path.basename(file))

    return zip_path  # 返回 ZIP 文件路径

def handle_file_and_directory(file_obj):
    # 获取文件的临时存储路径
    input_path = file_obj.name

    # 获取文件名并构建输出路径
    base_name = os.path.basename(input_path)

    file_name_without_extension = os.path.splitext(base_name)[0]
    input_md_path = get_source_file_dir() + "\\output\\" + file_name_without_extension + ".md"
    #判断文件是否存在
    if os.path.exists(input_md_path):
        print(f"文件 {input_md_path} 存在。")
    else:
        print(f"文件 {input_md_path} 不存在。开始生成markdown文件")
        pdf_to_markdown.process_pdf(input_path,get_source_file_dir() + "\\output")

    # 返回处理结果
    # return f"File copied to {output_path}"

    prefix = os.path.dirname(input_path)

    lines = get_lines(input_md_path)

    last_outputs = []

    ptop = 0 # 小数据测试

    # 并行处理
    last_outputs = process_lines_parallel(lines)

    # file_name_without_extension
    # 交给string_processing生成markdown格式表格
    lis = list_to_markdown(file_name_without_extension, last_outputs)
    lis = [os.path.join("data_processing", x) for x in lis]
    lis = [x + ".md" for x in lis]
    zip_path = generate_zip(lis)
    return [
        f'完成，文件存储在 {zip_path}',  # 文本消息
        zip_path  # 要下载的文件路径
    ]


def save_config(
        baidu_api, baidu_secret, kimi_api, zhipu_api,tx_deepseek_api,
        model_radio,
        pre_prompt, num_workers,ask_info_num,hash_num ,
        print_info,
        output_info,
        *ask_info_values,
):
    new_config = {
        "Baidu_api_key": baidu_api,
        "Baidu_Secret_key": baidu_secret,
        "kimi_api_key": kimi_api,
        "Zhipu_api_key": zhipu_api,
        "tx_deepseek_api_key": tx_deepseek_api,

        "model_type": model_radio,

        "pre_prompt": pre_prompt,
        "ask_info_num": ask_info_num,
        "ask_info": list(ask_info_values),
        "NUM_WORKERS": int(num_workers),
        "hash_num": int(hash_num),
        "print_info": int(print_info),
        "output_info": int(output_info)
    }

    write_configs(new_config)
    return "配置保存成功！请重新启动程序"

# 运行页面

def create_run_page():
    with gr.Blocks() as run_page:
        # 组件定义
        file_input = gr.File(label="选择输入文件")
        result_message = gr.Textbox(label="处理结果")
        download_btn = gr.DownloadButton(label="下载文件", visible=False)

        # 处理按钮
        process_btn = gr.Button("开始处理")

        # 点击事件
        @process_btn.click(
            inputs=[file_input],
            outputs=[result_message, download_btn]
        )
        def handle_process(file_obj):
            message, zip_path = handle_file_and_directory(file_obj)
            return [
                message,
                gr.DownloadButton(visible=True, value=zip_path)
            ]

    return run_page

# 设置界面

def create_config_page():
    config = load_configs()
    with gr.Blocks() as config_page:
        # config

        gr.Markdown("## 模型选择")
        model_radio = gr.Radio(
            choices=["kimi", "glm", "baidu", "tx_deepseek"],  # 根据实际情况调整模型选项
            value=config.get("model_name", config["model_type"]),  # 默认值
            label="选择主要使用的大模型"
        )

        gr.Markdown("## API密钥配置")
        with gr.Row():
            baidu_api = gr.Textbox(config["Baidu_api_key"], label="百度API Key")
            baidu_secret = gr.Textbox(config["Baidu_Secret_key"], label="百度Secret Key")
        with gr.Row():
            kimi_api = gr.Textbox(config["kimi_api_key"], label="Kimi API Key")
            zhipu_api = gr.Textbox(config["Zhipu_api_key"], label="智谱API Key")
        with gr.Row():
            tx_deepseek_api = gr.Textbox(config["tx_deepseek_api_key"], label="腾讯云deepseek API Key")

        gr.Markdown("## 提示信息配置")
        pre_prompt = gr.TextArea(config["pre_prompt"], label="前置提示语", lines=4)

        gr.Markdown("## 问答信息配置（ask_info）")
        ask_info_components = []

        ask_info_num = gr.Number(config["ask_info_num"], label="询问与提示词轮数", precision=0)

        for i in range(ask_info_num.value):
            with gr.Accordion(f"ask_info[{i}]", open=False):
                try:
                    ask_info_components.append(
                        gr.TextArea(config["ask_info"][i], lines=5, show_label=False)
                    )
                except IndexError:
                    ask_info_components.append(
                        gr.TextArea('new ask_info', lines=5, show_label=False)
                    )

        gr.Markdown("## 系统配置")
        num_workers = gr.Number(config["NUM_WORKERS"], label="工作线程数", precision=0)
        hash_num = gr.Number(config["hash_num"], label="是否备份", precision=0)
        print_info = gr.Number(config["print_info"], label="是否输出中间轮次回复", precision=0)
        output_info = gr.Number(config["output_info"], label="是否文件输出中间轮次回复", precision=0)

        gr.Markdown("## 操作区")
        save_btn = gr.Button("保存配置", variant="primary")
        status = gr.Textbox(interactive=False, label="操作状态")

        inputs = [
            baidu_api, baidu_secret, kimi_api, zhipu_api,tx_deepseek_api,
            model_radio,
            pre_prompt, num_workers,ask_info_num,hash_num,
            print_info,
            output_info,
            *ask_info_components,
        ]

        save_btn.click(
            save_config,
            inputs=inputs,
            outputs=status
        )
    return config_page

# 测试界面

def create_test_page():
    config = load_configs()

    ask_info_num = gr.Number(config["ask_info_num"], label="询问与提示词轮数", precision=0)
    ask_info_components = []
    for i in range(ask_info_num.value):
        with gr.Accordion(f"ask_info[{i}]", open=False):
            try:
                ask_info_components.append(
                    gr.TextArea(config["ask_info"][i], lines=5, show_label=False)
                )
            except IndexError:
                ask_info_components.append(
                    gr.TextArea('new ask_info', lines=5, show_label=False)
                )

# 创建Gradio界面
with gr.Blocks() as demo:
    with gr.Tab("运行界面", id=0):
        create_run_page()
    with gr.Tab("系统设置", id=1):
        create_config_page()

def start():
    # 使用show_error=True在控制台显示错误信息。
    print("端口为8080")
    demo.launch(server_name='0.0.0.0', server_port=8080, show_error=True)

if __name__ == "__main__":

    # multiprocessing.freeze_support()

    # 启动Gradio应用
    # 使用show_error=True在控制台显示错误信息。
    print("端口为8080")
    demo.launch(server_name='0.0.0.0', server_port=8080, show_error=True)

def start():

    # 使用show_error=True在控制台显示错误信息。
    print("端口为8080")
    demo.launch(server_name='0.0.0.0', server_port=8080, show_error=True)