# ChatPDF：一个交互式PDF查询工具
## 概述
ChatPDF是一个交互式工具，允许您上传PDF文件并根据其中的内容提问。它采用强大的技术堆栈，有效地对PDF进行分段，分析文本内容，并使用GPT-3.5提供准确的答案。

## 技术堆栈
**后端**：Python，FastAPI
**自然语言处理**：Langchain，GPT-3.5，Chroma
**前端**：Vue.js

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
### 先决条件
Git
Docker

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
echo "OPENAI_API_KEY=您的OpenAI_API密钥" > .env
```
将您的_openai_api_key_here 替换为您实际的 OpenAI API 密钥。

#### 使用 Docker 运行
```
docker-compose up
```

## 使用方法
设置完成后，打开您的网络浏览器，访问：
```
http://localhost:8080/
```

# ChatPDF: An Interactive PDF Query Tool
## Overview
ChatPDF is an interactive tool that allows you to upload PDF files and ask questions based on the content within them. Built with a robust tech stack, it efficiently segments PDFs, analyzes textual context, and provides accurate answers using GPT-3.5.

## Tech Stack
**Backend**: Python, FastAPI
**Natural Language Processing**: Langchain, GPT-3.5, Chroma
**Frontend**: Vue.js


## Features
- Upload PDF files for analysis.
- Ask questions based on the content within the PDF.
- Utilizes vector similarity and GPT-3.5 for accurate answers.


## How It Works
- PDF Segmentation: The uploaded PDF is divided into multiple chunks.
- Vectorization: These chunks are then converted into textual vectors.
- User Query: The user's question is also converted into a vector.
- Similarity Calculation: The vectors of the user's query and PDF text chunks are compared for similarity.
- Answer Generation: The most relevant text chunks are fed into GPT-3.5 along with the user query to generate the most accurate answer.


## Installation
### Prerequisites
Git
Docker
### Steps
#### Clone the Repository
```
git clone git@github.com:jhrsya/chatpdf.git
```
#### Navigate to Project Directory
```
cd chatpdf
```
#### Create .env File
Create a new .env file in the chatpdf directory to store your OpenAI API key:
```
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```
Replace your_openai_api_key_here with your actual OpenAI API key.

#### Run with Docker
```
docker-compose up
```

## Usage
After setting up, open your web browser and go to:
```
http://localhost:8080/
```






