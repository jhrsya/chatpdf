import gradio as gr
import requests

API_URL_UPLOAD = "http://localhost:8000/upload_files"
API_URL_CHAT = "http://localhost:8000/chat_file"
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

# 多轮对话处理
def chat_with_pdf(history, user_input):
    if user_input:
        # 构造请求体，包含当前输入和对话历史
        messages = [{"user": item[0], "assistant": item[1]} for item in history if item[1] is not None]
        response = requests.post(
            API_URL_CHAT,
            json={"message": user_input, "history": messages}
        )
        if response.status_code == 200:
            data = response.json()
            assistant_response = data["answer"]
            # 将新的一轮对话追加到历史中
            history.append((user_input, assistant_response))
            return history
        else:
            history.append((user_input, "获取回答失败，请重试！"))
            return history

with gr.Blocks() as demo:
    gr.Markdown("# PDF 多轮对话 Demo")

    with gr.Row():
        pdf_upload = gr.File(label="上传 PDF 文件", file_types=[".pdf"], interactive=True)
        upload_output = gr.Textbox(label="上传状态", interactive=False)

    pdf_upload.change(upload_file, inputs=[pdf_upload], outputs=[upload_output])

    with gr.Row():
        chatbot = gr.Chatbot(label="对话框")
        with gr.Column(scale=1):
            user_input = gr.Textbox(label="输入问题", placeholder="请输入你的问题...，按Enter键发送", interactive=True)
            chat_button = gr.Button("发送问题")

    user_input.submit(chat_with_pdf, inputs=[chatbot, user_input], outputs=[chatbot], queue=False)
    chat_button.click(chat_with_pdf, inputs=[chatbot, user_input], outputs=[chatbot], queue=False)

demo.launch()
