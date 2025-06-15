FROM python:3.11-slim

WORKDIR /app

COPY ./frontend/frontend.py .

RUN pip install --no-cache-dir streamlit requests streamlit-authenticator

EXPOSE 8501

# CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]
