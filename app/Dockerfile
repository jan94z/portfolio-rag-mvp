FROM python:3.10-slim

WORKDIR /root

# System deps for PDF parsing and some Python packages
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc libglib2.0-0 libsm6 libxext6 libxrender-dev \
#     && rm -rf /var/lib/apt/lists/*
RUN rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker cache efficiency
COPY ./app/requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download Hugging Face model so container is ready at startup, then clear cache
# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
# RUN rm -rf /root/.cache

# Copy application code
COPY ./app /root/app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]