FROM python:3.10.2

WORKDIR /usr/src/mai-backend

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "core.py"]
