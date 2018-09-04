FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
ADD . /app/
WORKDIR /app
RUN pip install pipenv
RUN pipenv install --system
