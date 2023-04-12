FROM python:3.10.8-bullseye

ENV \
    PYTHONPATH=/usr/local/bin/python3 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p /auth_api
COPY ./ /auth_api
RUN \
    pip install --upgrade wheel \
    && python3 -m pip install -r /auth_api/requirements.txt

WORKDIR /auth_api

