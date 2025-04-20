import os

from magic_pdf.config.enums import SupportedPdfParseMethod
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze


def process_pdf(pdf_position, output_position):
    # output_position = os.path.dirname(pdf_position) + "\\output"

    # 提取文件名（不带扩展名）
    pdf_file_name = os.path.basename(pdf_position)
    name_without_suff = os.path.splitext(pdf_file_name)[0]

    # 准备输出环境
    local_image_dir = os.path.join(output_position, "images")
    local_md_dir = output_position

    os.makedirs(local_image_dir, exist_ok=True)

    image_writer = FileBasedDataWriter(local_image_dir)
    md_writer = FileBasedDataWriter(local_md_dir)

    # 读取PDF内容
    reader = FileBasedDataReader("")  # 注意：这里的空字符串可能需要根据实际情况调整
    pdf_bytes = reader.read(pdf_position)

    # 创建数据集实例
    ds = PymuDocDataset(pdf_bytes)

    # 推理
    if ds.classify() == SupportedPdfParseMethod.OCR:
        infer_result = ds.apply(doc_analyze, ocr=True)
        pipe_result = infer_result.pipe_ocr_mode(image_writer)
    else:
        infer_result = ds.apply(doc_analyze, ocr=False)
        pipe_result = infer_result.pipe_txt_mode(image_writer)

    # 在每一页上绘制模型结果
    infer_result.draw_model(os.path.join(local_md_dir, f"{name_without_suff}_model.pdf"))

    # 在每一页上绘制布局结果
    pipe_result.draw_layout(os.path.join(local_md_dir, f"{name_without_suff}_layout.pdf"))

    # 在每一页上绘制span结果
    pipe_result.draw_span(os.path.join(local_md_dir, f"{name_without_suff}_spans.pdf"))

    # 导出Markdown
    pipe_result.dump_md(md_writer, f"{name_without_suff}.md", os.path.basename(local_image_dir))

    # 导出内容列表
    pipe_result.dump_content_list(md_writer, f"{name_without_suff}_content_list.json",
                                  os.path.basename(local_image_dir))


# 使用示例
# pdf_path = "C:/Users/Administrator/Desktop/code/python/pythonProject2/test.pdf"
# output_path = "C:/Users/Administrator/Desktop/code/python/pythonProject2/output"
# process_pdf(pdf_path, output_path)