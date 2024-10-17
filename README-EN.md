# ChatPDF: An Interactive PDF Query Tool
[ENGLISH VERSION](README-EN.md)

## Overview
ChatPDF is an interactive tool that allows you to upload PDF files and ask questions based on their content. It leverages a powerful tech stack to efficiently segment PDFs, analyze textual content, and provide accurate answers using GPT-3.5.

## Tech Stack
- **Backend**: Python, FastAPI  
- **Natural Language Processing**: Langchain, GPT-3.5, Chroma  
- **Frontend**: gradio

## Features
- Upload PDF files for analysis.
- Ask questions based on the content of the PDF.
- Provide accurate answers using vector similarity and GPT-3.5.

## How It Works
- **PDF Segmentation**: The uploaded PDF is divided into multiple chunks.
- **Vectorization**: These chunks are then converted into text vectors.
- **User Query**: The user’s question is also converted into a vector.
- **Similarity Calculation**: The user query vector is compared with the vectors of the PDF text chunks to find the most relevant sections.
- **Answer Generation**: The most relevant text chunks are combined with the user query and fed into GPT-3.5 to generate the most accurate answer.

## Installation

### Prerequisites
- Git

### Steps

#### Clone the Repository
```
git clone git@github.com:jhrsya/chatpdf.git
```

#### Navigate to the Project Directory
```
cd chatpdf
```

#### Create a .env File
In the `chatpdf` directory, create a new `.env` file to store your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```
Replace `your_openai_api_key_here` with your actual OpenAI API key.

#### Launch

1. Start the Backend
```
cd api
python main.py
```

2. Start the Frontend
```
cd front
python ui.py
```

3. Access the app at [http://127.0.0.1:7860](http://127.0.0.1:7860) to start