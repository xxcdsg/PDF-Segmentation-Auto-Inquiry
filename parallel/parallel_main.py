import threading
import queue
import config

from ask_one_line import ask_one_line, ask_one_line_mul
from config.config import load_configs

configs = load_configs()
NUM_WORKERS = configs['NUM_WORKERS']

def process_lines_parallel(lines, num_workers=NUM_WORKERS):
    # ================== 初始化基础设施 ==================
    task_queue = queue.Queue()  # 线程安全的任务队列
    print_lock = threading.Lock()  # 保证打印不混乱的锁
    results = [None] * len(lines)  # 预分配结果存储（索引对应行号）

    # ================== 工作线程定义 ==================
    def worker():
        while True:
            # 获取任务（自动阻塞等待）
            line_number, line = task_queue.get()

            # 终止信号处理
            if line is None:
                task_queue.task_done()
                break

            # 打印处理进度（带锁保护）
            with print_lock:
                print(f"asking {line_number + 1} line")  # ptop从1开始计数
                # print("原文为:", line)

            # 空行处理逻辑
            if not line.strip():
                with print_lock:
                    print("该行为空行")
                results[line_number] = None
                task_queue.task_done()
                continue

            # 实际处理逻辑（替换为你的API调用）
            if configs["output_info"] == 1:
                data = ask_one_line_mul(line)
            else :
                data = ask_one_line(line)

            with print_lock:
                print(f"over {line_number + 1} line")
                # print("该行的结果为\n", data)

            results[line_number] = data
            task_queue.task_done()

    # ================== 启动线程池 ==================
    # 预先填装所有任务（带行号）
    for i, line in enumerate(lines):
        task_queue.put((i, line))

    # 创建并启动工作线程
    threads = []
    for _ in range(num_workers):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    # ================== 等待任务完成 ==================
    task_queue.join()  # 阻塞直到所有任务完成

    # ================== 清理线程池 ==================
    for _ in range(num_workers):  # 发送终止信号
        task_queue.put((0, None))

    for t in threads:  # 等待线程退出
        t.join()

    # 过滤空结果（保持与原逻辑一致）
    return [data for data in results if data is not None]
