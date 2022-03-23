FROM python:3.10.2

WORKDIR /usr/src/mai-api

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "server.py"]
