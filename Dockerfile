FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements/prod.txt /app/
RUN pip install -r prod.txt
ADD . /app/
