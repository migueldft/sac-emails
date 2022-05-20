FROM python:3.8-slim-buster

RUN apt-get -y update && apt-get install -y --no-install-recommends \
        wget \
        python3 \
        nginx \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip --no-cache-dir install sklearn catboost pandas fastparquet joblib unidecode nltk flask gunicorn

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

COPY src /opt/program
WORKDIR /opt/program