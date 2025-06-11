FROM python:3.10-slim

WORKDIR /app

# System dependencies for PDF parsing (optional, adjust as needed)
RUN apt-get update && apt-get install -y gcc libglib2.0-0 libsm6 libxext6 libxrender-dev && rm -rf /var/lib/apt/lists/*

COPY ./app /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
