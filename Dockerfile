ARG BASE_IMAGE=ubuntu:18.04
#ARG BASE_IMAGE=pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime

FROM ${BASE_IMAGE}

WORKDIR /tmp

COPY ./cndocker/ubuntu18.04-sources.list /etc/apt/sources.list
COPY ./cndocker/pip.conf /root/.pip/pip.conf
COPY requirements.txt .

RUN apt update ;\
    apt install -y python3 python3-pip python3-dev uwsgi uwsgi-plugin-python3 ;\
    apt autoremove ;\
    apt clean

RUN pip3 install --no-cache \
                 -U pip setuptools

RUN pip3 install --no-cache \
                 supervisor==4.2.2 \
                 click==7.1.2 \
                 label-studio-ml==1.0.3 \
                 -r requirements.txt


COPY uwsgi.ini.plugin-mode /etc/uwsgi/uwsgi.ini
COPY supervisord.conf /etc/supervisor/conf.d/

COPY . /app/

EXPOSE 9090

WORKDIR /app

ENV MODEL_DIR=/maas_storage/model
ENV RQ_QUEUE_NAME=default
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV USE_REDIS=1

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]