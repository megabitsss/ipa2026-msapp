FROM python:3.14-slim
WORKDIR /home/worker
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "/home/worker/consumer.py"]
