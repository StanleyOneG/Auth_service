FROM python:3.10.8-bullseye

ENV \
    PYTHONPATH=/usr/local/bin/python3 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p /auth_api
# COPY ./ /auth_api
COPY ./requirements.txt /auth_api
RUN \
    pip install --upgrade wheel \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install -r /auth_api/requirements.txt

WORKDIR /auth_api

EXPOSE 8000
ENV FLASK_APP="main"

CMD \
    python -m flask db upgrade \
    && python -m flask create_superuser \
    # && gunicorn main:app -w 2 -b 0.0.0.0:8000\
    && python main.py 