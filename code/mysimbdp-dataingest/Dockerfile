FROM python:3.8.2

WORKDIR /app

COPY requirements.txt .
COPY producer.py .
COPY credentials.cfg .

ENV CASSANDRA_HOST="host.docker.internal"

RUN pip install -r requirements.txt

CMD ["python", "producer.py"]
