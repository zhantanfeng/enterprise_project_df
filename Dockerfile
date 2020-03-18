FROM python:3.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
CMD ["python","app.py"]

