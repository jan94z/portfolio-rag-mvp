FROM python:3.11-slim

WORKDIR /root

COPY ./frontend/requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir -r /root/requirements.txt

# COPY ./frontend /root/frontend



EXPOSE 8501

CMD ["streamlit", "run", "./frontend/Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]
