FROM python:latest

WORKDIR /usr/src/app

COPY /Pipfile /Pipfile.lock ./

RUN pip install -U pipenv \
    && pipenv install --system


COPY /entrypoint.sh /usr/src/app/entrypoint.sh

COPY . .