FROM python:3.9-slim AS worker-magnet

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "worker.py"]
