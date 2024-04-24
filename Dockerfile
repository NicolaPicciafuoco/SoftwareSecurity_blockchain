FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /app/static

COPY contract /app/contract
COPY core /app/core
COPY Healthcare /app/Healthcare
COPY Management_Prestazioni /app/Management_Prestazioni
COPY Management_Terapia /app/Management_Terapia
COPY Management_User /app/Management_User
COPY templates /app/templates
COPY manage.py .

