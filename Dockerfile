#ARG BASE_IMAGE=ubuntu:18.04
#ARG BASE_IMAGE=pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime
ARG BASE_IMAGE=fudannlp/fudannlp:pytorch1.9.0-cuda11.1-cudnn8-runtime-sshd-ceph

FROM ${BASE_IMAGE}

WORKDIR /tmp

COPY ./cndocker/ubuntu18.04-sources.list /etc/apt/sources.list
COPY ./cndocker/pip.conf /root/.pip/pip.conf
COPY requirements.txt .

RUN pip install --no-cache \
                -r requirements.txt \
                uwsgi==2.0.19.1 \
                supervisor==4.2.2 \
                click==7.1.2 \
                label-studio-ml==1.0.3

COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/supervisor/conf.d/

WORKDIR /app

COPY . /app/

EXPOSE 9090

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]