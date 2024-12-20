# ChatPDF：一个交互式PDF查询工具
[ENGLISH VERSION](README-EN.md)
## 概述
ChatPDF是一个交互式工具，允许您上传PDF文件并根据其中的内容提问。它采用强大的技术堆栈，有效地对PDF进行分段，分析文本内容，并使用GPT-3.5提供准确的答案。

## 技术堆栈
- **后端**：Python，FastAPI  
- **自然语言处理**：Langchain，GPT-3.5，Chroma  
- **前端**：gradio

## 特点
- 上传PDF文件进行分析。
- 基于PDF内容提出问题。
- 利用向量相似性和GPT-3.5提供准确答案。

## 工作原理
- PDF分段：上传的PDF被分割成多个块。
- 向量化：然后将这些块转换为文本向量。
- 用户查询：用户的问题也被转换为向量。
- 相似性计算：将用户查询的向量与PDF文本块的向量进行相似性比较。
- 答案生成：将最相关的文本块与用户查询一起输入GPT-3.5，生成最准确的答案。

## 安装
### 前提条件
- Git

### 步骤
#### 克隆存储库
```
git clone git@github.com:jhrsya/chatpdf.git
```
#### 导航至项目目录
```
cd chatpdf
```
#### 创建 .env 文件
在 chatpdf 目录中创建一个新的 .env 文件，用于存储您的 OpenAI API 密钥：
```
OPENAI_API_KEY=your_openai_api_key_here
```
将your_openai_api_key_here替换为您实际的 OpenAI API 密钥。


#### 创建环境
```
conda create -n chatpdf python=3.10
conda activate chatpdf
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
cd chatpdf
pip install -r requirement.txt
```

#### 启动
1. 启动后端
```
cd api
python main.py
```

2. 启动前端
```
cd front
python ui.py
```


3. 点击http://127.0.0.1:7860启动
