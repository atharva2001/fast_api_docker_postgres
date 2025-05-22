FROM python:3.12-slim

WORKDIR /fastapi_app/src

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    redis-server

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

EXPOSE 8000 

COPY . .

CMD [ "python3", "app.py" ]