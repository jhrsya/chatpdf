import gradio as gr
import requests
import json

# FastAPI 后端地址
backend_url = "http://localhost:8000"

def upload_file(file):
    """上传文件到 FastAPI 端点"""
    try:
        with open(file.name, 'rb') as f:
            files = {'file': (file.name, f, 'multipart/form-data')}
            response = requests.post(f"{backend_url}/upload_files", files=files)
        return response.text
    except Exception as e:
        return str(e)


def chat_with_file(message):
    """发送聊天消息到 FastAPI 端点并返回响应"""
    try:
        data = {"message": message}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{backend_url}/chat_file", data=json.dumps(data), headers=headers)
        return response.json()
    except Exception as e:
        return str(e)


def test_message(message):
    """发送简单的测试消息到 FastAPI 端点"""
    try:
        data = {"message": message}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{backend_url}/test", data=json.dumps(data), headers=headers)
        return response.text
    except Exception as e:
        return str(e)


# Gradio UI 设置
with gr.Blocks() as demo:
    gr.Markdown("## 文件聊天应用")

    with gr.Tab("上传文件"):
        file_input = gr.File(label="上传文件")
        upload_button = gr.Button("上传")
        upload_output = gr.Textbox(label="上传状态")

        upload_button.click(fn=upload_file, inputs=file_input, outputs=upload_output)

    with gr.Tab("发送消息"):
        message_input = gr.Textbox(label="输入消息")
        chat_button = gr.Button("发送")
        chat_output = gr.Textbox(label="回答")

        chat_button.click(fn=chat_with_file, inputs=message_input, outputs=chat_output)

    with gr.Tab("测试端点"):
        test_input = gr.Textbox(label="测试消息")
        test_button = gr.Button("发送")
        test_output = gr.Textbox(label="测试返回")

        test_button.click(fn=test_message, inputs=test_input, outputs=test_output)

# 启动 Gradio 应用
demo.launch()
