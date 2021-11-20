FROM python:3.7-slim-buster

ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements/celery.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf requirements.txt

RUN mkdir -p /api
COPY ./api /api
COPY ./dockers/celery/run_celery.sh /run_celery.sh
RUN chmod a+rwx /run_celery.sh && chmod -R a+rwx /api

WORKDIR /api