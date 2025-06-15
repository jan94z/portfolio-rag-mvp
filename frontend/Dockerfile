FROM python:3.11-slim

WORKDIR /app

# COPY ./frontend/* .

RUN pip install --no-cache-dir streamlit requests streamlit-authenticator

EXPOSE 8501

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]
