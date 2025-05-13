FROM python:3.9-slim AS worker-magnet

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY worker.py .

CMD ["python", "worker.py"]
