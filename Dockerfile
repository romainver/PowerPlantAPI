FROM python:latest
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
WORKDIR /code