from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile
import uvicorn
import os
from pydantic import BaseModel
from qa_chat import (
    get_answer_from_chain, 
    get_similar_docs_from_chroma,
    create_index_by_chroma,
    get_documents_from_bytes, 
    read_index_by_chroma
)
from utils.constant import UPLOAD_DIR, CHROMA_PATH
from langchain.chains.question_answering import load_qa_chain
import json
from utils.tools import validate_index_name
from dotenv import load_dotenv
from typing import List


# 加载 .env 文件中的环境变量
load_dotenv()


app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class UserMessage(BaseModel):
    message: str

class ChatHistory(BaseModel):
    history: List[dict]
    message: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/test")
async def test_endpoint(msg: UserMessage):
    return "Hello World" + msg.message





@app.post("/chat_file")
async def chat_file(msg: ChatHistory):

    # 读取文件名
    with open(os.path.join(UPLOAD_DIR, "file_name.json"), "r") as f:
        fread = json.load(f)
        file_name = fread["file_name"]

    # 拼接对话历史到当前问题
    conversation_context = ""
    for item in msg.history:
        conversation_context += f"User: {item['user']}\nAssistant: {item['assistant']}\n"
    conversation_context += f"User: {msg.message}\n"

    # 获取与 query 相似的文档
    docs = get_similar_docs_from_chroma(query=conversation_context, 
                                        chroma_directory=os.path.join(CHROMA_PATH, file_name))

    # 生成答案
    answer = get_answer_from_chain(docs=docs, query=msg.message, load_chain=load_qa_chain)

    # 将当前对话保存到历史中
    new_history_entry = {"user": msg.message, "assistant": answer["output_text"]}
    msg.history.append(new_history_entry)

    return {"answer": answer["output_text"], "history": msg.history}



@app.post("/upload_files")
async def upload_file(file: UploadFile):
    """
    清空
    """
    try:
        # 创建新的Chroma数据库
        # index_name = validate_index_name(file.filename)
        index_name = file.filename
        # 修改文件名
        with open(os.path.join(UPLOAD_DIR, "file_name.json"), "w") as f:
            json.dump({"file_name": index_name}, f, indent=4)
        # 读取文件内容为字节数据
        bytes_data = await file.read()
        # 读取数据
        documents = get_documents_from_bytes(bytes_data=bytes_data, source=index_name)
        # 创建Chroma数据库
        
        create_index_by_chroma(documents=documents, 
                               chroma_directory=os.path.join(CHROMA_PATH, index_name))

        return "upload success"
    except Exception as e:
        raise e
        return "upload failed"




# Run this script with: uvicorn script_name:app --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)