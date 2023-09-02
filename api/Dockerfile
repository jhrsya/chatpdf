# FROM python
FROM python:3.10-slim-buster

# 安装chroma需要这条命令
RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential

# 把当前目录所有文件拷贝到docker的/app目录下
COPY . /app

# 切换工作目录为/app
WORKDIR /app

# 安装构件app所需要的package
RUN pip install -r requirements.txt

# 运行应用
CMD ["python", "main.py", ">","log.txt"]