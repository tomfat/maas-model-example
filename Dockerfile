ARG BASE_IMAGE=ubuntu:18.04
#ARG BASE_IMAGE=pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime

# 安装所需依赖
FROM ${BASE_IMAGE} AS RUNTIME

WORKDIR /tmp

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY ./cndocker/ubuntu18.04-tsinghua-source.list /etc/apt/sources.list

RUN apt update ;\
    apt install -y python3 python3-pip python3-dev uwsgi uwsgi-plugin-python3 ;\
    apt autoremove ;\
    apt clean

COPY ./cndocker/pip-tsinghua.conf /root/.pip/pip.conf
COPY ./app/requirements.txt .

RUN pip3 install --no-cache \
                 -U pip setuptools

RUN pip3 install --no-cache \
                 supervisor==4.2.2 \
                 click==7.1.2 \
                 label-studio-ml==1.0.3 \
                 -r requirements.txt

COPY ./app /app/

WORKDIR /app

# 执行单元测试
#FROM RUNTIME
#
#COPY ./test /test
#
#RUN pip3 install --no-cache pytest pytest-dependency
#
#RUN python3 -m pytest /test/*

# 构造最终镜像
FROM RUNTIME

COPY wsgi/uwsgi.ini.plugin-mode /etc/uwsgi/uwsgi.ini
COPY wsgi/supervisord.conf /etc/supervisor/conf.d/
COPY wsgi/_wsgi.py /app/_wsgi.py

ENV MODEL_DIR=/var/maas-storage
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379
ENV RQ_QUEUE_NAME=default
ENV PYTHONPATH=/app:/app/tacred-relation

EXPOSE 9090

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
