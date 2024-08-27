FROM python:3.11-slim-buster as builder

WORKDIR /app

COPY /'requirements.txt' /

RUN pip install -r /'requirements.txt' --no-cache-dir

COPY . .
