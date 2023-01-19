FROM python:3.9

RUN mkdir /backend

WORKDIR /backend

COPY requirements.txt /backend/requirments.txt

RUN pip install --upgrade pip && pip install -r requirments.txt

COPY . .