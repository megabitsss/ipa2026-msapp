FROM python:3.14-slim
WORKDIR /home/scheduler
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "/home/scheduler/scheduler.py"]
