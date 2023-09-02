# ChatPDF: An Interactive PDF Query Tool
## Overview
ChatPDF is an interactive tool that allows you to upload PDF files and ask questions based on the content within them. Built with a robust tech stack, it efficiently segments PDFs, analyzes textual context, and provides accurate answers using GPT-3.5.

## Tech Stack
- **Backend**: Python, FastAPI
- **Natural Language Processing**: Langchain, GPT-3.5, Chroma
- **Frontend**: Vue.js


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
- Git
- Docker
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