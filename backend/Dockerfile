FROM python:3.8

COPY . /

WORKDIR /

ENV PYTHONPATH=/

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

CMD gunicorn -c gunicorn_conf.py -b 127.0.0.1:5000 app:"create_app('production')"