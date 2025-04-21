import zipfile

import gradio as gr
import os
import pdf_to_markdown
from config.config import load_configs, write_configs
from data_processing.string_processing import list_to_markdown
from markdown_read import get_lines
from parallel.parallel_main import process_lines_parallel
from typing import List

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
            else:
                print("file not found",file)

    return zip_path  # 返回 ZIP 文件路径


def process_single_pdf(pdf_path: str, output_dir: str) -> List[str]:
    """处理单个PDF文件并返回生成的文件列表"""
    base_name = os.path.basename(pdf_path)
    file_name_without_extension = os.path.splitext(base_name)[0]
    input_md_path = os.path.join(output_dir, f"{file_name_without_extension}.md")

    if not os.path.exists(input_md_path):
        print(f"正在转换: {base_name} 为Markdown...")
        pdf_to_markdown.process_pdf(pdf_path, output_dir)

    lines = get_lines(input_md_path)
    last_outputs = process_lines_parallel(lines)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    lis = list_to_markdown(file_name_without_extension, last_outputs)
    lis = [os.path.join(base_dir,"data_processing", x) for x in lis]
    lis = [x + ".md" for x in lis]

    return lis

def handle_files_and_directories(file_objs):
    output_dir = os.path.join(get_source_file_dir(), "output")
    os.makedirs(output_dir, exist_ok=True)

    all_output_files = []
    processed_files = []
    failed_files = []

    for file_obj in file_objs:
        try:
            if file_obj.name.lower().endswith('.pdf'):
                files = process_single_pdf(file_obj.name, output_dir)
                all_output_files.extend(files)
                processed_files.append(os.path.basename(file_obj.name))
        except Exception as e:
            failed_files.append(f"{os.path.basename(file_obj.name)}: {str(e)}")
            continue

    if not all_output_files:
        return ["没有生成任何文件，请检查输入文件", None]

    zip_path = generate_zip(all_output_files)

    message = "处理完成！\n"
    if processed_files:
        message += f"成功处理文件：\n" + "\n".join(processed_files) + "\n\n"
    if failed_files:
        message += f"处理失败文件：\n" + "\n".join(failed_files)

    return [message, zip_path]


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

# 修改后的运行界面
def create_run_page():
    with gr.Blocks() as run_page:
        with gr.Row():
            file_input = gr.File(
                label="选择PDF文件或文件夹",
                file_count="multiple",
                file_types=[".pdf", "folder"]
            )
        result_message = gr.Textbox(label="处理结果")
        download_btn = gr.DownloadButton(label="下载处理结果", visible=False)
        process_btn = gr.Button("开始批量处理", variant="primary")

        @process_btn.click(
            inputs=[file_input],
            outputs=[result_message, download_btn]
        )
        def handle_process(file_objs):
            if not file_objs:
                return ["请先选择文件或文件夹", None]

            message, zip_path = handle_files_and_directories(file_objs)
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