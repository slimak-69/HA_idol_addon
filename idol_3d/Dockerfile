ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.12-alpine3.20
FROM ${BUILD_FROM}

WORKDIR /app

RUN pip install --no-cache-dir \
    flask==3.0.3 \
    requests==2.32.3 \
    gunicorn==23.0.0

COPY app.py /app/app.py

CMD ["gunicorn", "--bind", "0.0.0.0:8099", "--workers", "2", "--timeout", "300", "app:app"]
