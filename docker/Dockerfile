# syntax=docker/dockerfile:1.4
# Build the Python CLI app image
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY app/ app/

CMD ["python", "-m", "app.interface.cli"]

