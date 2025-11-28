# Minimal generator image using Python slim
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    SERIES_PATH=/config/series.yaml \
    INTERVAL_SEC=5

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py /app/

EXPOSE 8080
CMD ["python", "app.py"]
