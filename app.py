from flask import Flask,render_template,url_for,Response
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import asyncio
import json
import tracemalloc
from datetime import datetime, timezone
from utils.read import *
from loglizer.benchmarks import HDFS_bechmark
import requests
import threading
import time
import socket
import pandas as pd
from io import StringIO
import dask.dataframe as dd

app = Flask(__name__)
tracemalloc.start()

@app.route('/')
def hello_world():
    return render_template("index.html")

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = set(['cap', 'pcap', 'csv', 'log'])  # 允许上传的文件后缀

# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 具有上传功能的页面
@app.route('/onload.html')
def upload_onload():
    return render_template('onload.html')

# 具有上传功能的页面
@app.route('/detection.html')
def upload_detection():
    return render_template('detection.html')

#监听
@app.route('/dashboard-2.html')
def upload_monitor():
    return render_template('dashboard-2.html')

#数据层分析
@app.route('/anadata.html')
def anlydata_monitor():
    return render_template('anadata.html')

#主页
@app.route('/index.html')
def anlydata_index():
    return render_template('index.html')

#多维结合层分析
@app.route('/anamulti_zlzr.html')
def anlymulti_monitor():
    return render_template('anamulti_zlzr.html')

#控制层分析
@app.route('/anafuncode.html')
def anlyfunc_monitor():
    return render_template('anafuncode.html')

#表格
@app.route('/tables-main.html')
def upload_table():
    return render_template('tables-main.html')

#滚动
@app.route('/extra-scrollbox.html')
def upload_scrollbox():
    return render_template('extra-scrollbox.html')

#数据表
@app.route('/tables-datatable.html')
def upload_datatable():
    return render_template('tables-datatable.html')

#忘了
@app.route('/forms-sliders.html')
def upload_sliders():
    return render_template('forms-sliders.html')

#上传文件看结果
@app.route('/layout-mixed-menus.html')
def upload_dashboard():
    return render_template('layout-mixed-menus.html')

#按钮
@app.route('/forms-buttons.html')
def upload_buttons():
    return render_template('forms-buttons.html')

#chart
@app.route('/charts.html')
def upload_chart():
    return render_template('charts.html')

@app.route('/test.json')
def upload_facicon():
    return render_template('test.json')

@app.route('/skin-black.html')
def upload_upfile():
    return render_template('skin-black.html')

@app.route('/skin-white.html')
def upload_white():
    return render_template('skin-white.html')

@app.route('/skin-green.html')
def upload_green():
    return render_template('skin-green.html')

@app.route('/anamulti_none.html')
def upload_anamulti_none():
    return render_template('anamulti_none.html')

@app.route('/skin-cafe.html')
def upload_cafe():
    return render_template('skin-cafe.html')

@app.route('/skin-red.html')
def upload_red():
    return render_template('skin-red.html')

@app.route('/skin-purple.html')
def upload_purple():
    return render_template('skin-purple.html')

@app.route('/skin-blue.html')
def upload_blue():
    return render_template('skin-blue.html')

@app.route('/skin-yellow.html')
def upload_yellow():
    return render_template('skin-yellow.html')


@app.route('/get_filename', methods=['GET'], strict_slashes=False)
def api_upfilename():
    folder = request.args.get('folder')
    name_list = get_finame(folder)
    return jsonify(name_list)


@app.route('/get_file_count', methods=['GET'], strict_slashes=False)
def api_file_count():
    folder_name = request.args.get('folder')
    print(f"Received request for folder: {folder_name}")  # 调试信息
    print(f"All request args: {request.args}")  # 调试信息
    
    if folder_name is None:
        folder_name = 'upload'  # 默认值
        print(f"No folder specified, using default: {folder_name}")  # 调试信息
    
    file_count = get_file_count(folder_name)
    print(f"File count for {folder_name}: {file_count}")  # 调试信息
    return jsonify({'file_count': file_count})

#上传函数
@app.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    file = request.files['myfile']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(file_dir, filename)
        file.save(file_path)

        return jsonify({'filename': filename}) # 返回JSON响应
    else:
        return jsonify({'error': 'Invalid file type or file not provided'}), 400

@app.route('/get-logs', methods=['GET'])
def get_logs():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with open(file_path, 'r') as file:
            logs = parse_log_file(file_path)
            global log_entry_count
            log_entry_count = len(logs)
        return jsonify({
            'logs': logs,
            'log_entries_count': log_entry_count
        })
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


@app.route('/train_model', methods=['POST'])
def train_model():
    struct_log = request.form.get('struct_log')
    log_label = request.form.get('log_label')

    # 调用模型训练函数并获取 CSV 内容
    y_pred = HDFS_bechmark.model_using('upload/'+struct_log, 'upload/'+log_label)

    return jsonify(y_pred.tolist())


@app.route('/get-anomalies', methods=['POST'])
def get_anomalies():
    # 获取选中的文件名
    struct_log_file = request.form.get('struct_log')
    log_label_file = request.form.get('log_label')

    chunk_size = 1000  # 每块的大小
    anomaly_entries = []
    global_anomaly_indices = []
    print("struct_log_file:", struct_log_file)
    print("log_label_file:", log_label_file)
    # 读取标签文件并收集异常索引
    for i, chunk in enumerate(pd.read_csv(os.path.join('results/', log_label_file), chunksize=chunk_size)):
        anomaly_indices = chunk[chunk['status'] == 1].index
        global_anomaly_indices.extend(anomaly_indices + i * chunk_size)  # 转换为全局索引
    print("anomaly_indices:", anomaly_indices)
    print("global_anomaly_indices:", global_anomaly_indices)
    # 读取日志文件并根据全局索引获取异常条目
    log_df = pd.read_csv(os.path.join('upload/', struct_log_file))
    for index in global_anomaly_indices:
        if index < len(log_df):
            anomaly_entries.append(log_df.iloc[index].to_dict())
    print("anomaly_entries:", anomaly_entries)
    # 返回异常日志条目
    return jsonify(anomalies=anomaly_entries)

@app.route('/get_packet', methods=['GET'], strict_slashes=False)
def api_packet():
    def api_packet():
        filename = request.values.get('filename')
        Fname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        id = request.values.get('id')
        if not id:
            return jsonify({'error': 'No ID provided'}), 400
        path = os.path.join(Fname, filename)
        try:
            packet = get_one_packet(path, id)
            return packet  # 直接返回字符串数据
        except Exception as e:
            return str(e), 500  # 返回错误信息





if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)
    #热更新静态资源网页
    app.jinja_env.auto_reload = True
