FROM python:3.10.8-bullseye

ENV \
    PYTHONPATH=/usr/local/bin/python3 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

RUN mkdir -p /auth_tests

COPY ./ /auth_tests

RUN \
    groupadd -r tester && useradd -d /auth_tests -r -g tester tester \
    && chown tester:tester -R /auth_tests \
    && pip install --upgrade wheel \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install -r ./auth_tests/requirements.txt 


WORKDIR /auth_tests/functional

USER tester

ENTRYPOINT pytest src/