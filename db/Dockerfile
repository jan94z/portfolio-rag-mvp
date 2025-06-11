FROM python:3.11-slim

WORKDIR /app

COPY db/ /app

RUN pip install --no-cache-dir -r shared/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "ingestion.py"]