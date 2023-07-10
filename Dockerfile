FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE csvprocessing.settings
ENV ROOT_DIR /usr/src

WORKDIR $ROOT_DIR

COPY . $ROOT_DIR

RUN set -ex \
    && pip install --no-cache-dir --upgrade pip \
    && pip install -r $ROOT_DIR/requirements.txt --no-cache-dir