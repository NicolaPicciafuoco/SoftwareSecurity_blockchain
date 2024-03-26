FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /app/static

COPY ./contract .
COPY ./core .
COPY ./Healthcare .
COPY ./Management_Prestazioni .
COPY ./Management_User .
COPY db.sqlite3 .
COPY manage.py .

