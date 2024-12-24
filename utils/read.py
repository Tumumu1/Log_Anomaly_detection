import pyshark,os
from pyshark.tshark import tshark
from pyshark.tshark.tshark import get_tshark_interfaces, get_process_path
from collections import Counter
import numpy as np
import asyncio
import logging
import logging.handlers
import re
from datetime import datetime
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'log'

def parse_log_file(file_path):
    logs = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):  # 从1开始计数行号
            line = line.strip()
            if not line:
                continue  # 跳过空行

            # 按空格分割每行日志数据
            parts = line.split(" ")

            # 提取各个字段
            line_id = int(parts[0].replace("-", ""))
            timestamp = int(parts[1])
            date_str = parts[2]
            node = parts[3]
            datetime_str = " ".join(parts[4].split("-")[0:3])
            node_detail = parts[5]
            event_type_parts = parts[6:]
            event_type_capitalized = []
            message_lowercase = []

            for part in event_type_parts:
                if part.isupper():
                    event_type_capitalized.append(part)
                else:
                    message_lowercase.append(part)

            event_type = " ".join(event_type_capitalized)
            message = " ".join(message_lowercase)

            # 创建字典来存储解析后的数据
            log_entry = {
                'line_id': line_id,  # 行数
                'id': timestamp,
                'date': date_str,
                'node': node,
                'datetime': datetime_str,  # 可读的日期时间字符串
                'node_detail': node_detail,
                'event_type': event_type,
                'message': message.strip()  # 去除可能的前后空格
            }
            logs.append(log_entry)

    return logs


def get_finame(foldername):
    # 获取read.py所在的目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 回退到neonn目录
    neonn_dir = os.path.dirname(current_dir)
    # 构建upload文件夹的路径
    folder_path = os.path.join(neonn_dir, foldername)
    # 获取文件夹中的所有文件名
    file_names = os.listdir(folder_path)
    return file_names

def get_file_count(folder_name):
    # 获取read.py所在的目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 回退到neonn目录
    neonn_dir = os.path.dirname(current_dir)
    # 构建指定文件夹的路径
    folder_path = os.path.join(neonn_dir, folder_name)
    # 获取文件夹中的所有文件名
    try:
        file_names = os.listdir(folder_path)
        # 计算文件数目
        file_count = len([name for name in file_names if os.path.isfile(os.path.join(folder_path, name))])
        return file_count
    except Exception as e:
        print(f"Error counting files in {folder_name}: {str(e)}")
        return 0


def get_one_packet(path,id):
    cap = pyshark.FileCapture(path)
    if isinstance(id,str):
        id = int(id)
    return str(cap[id])
