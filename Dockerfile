FROM python:3.6.6-alpine3.8
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add python3-dev build-base linux-headers pcre-dev mariadb-dev 
ADD Pipfile /tmp
ADD Pipfile.lock /tmp

WORKDIR /tmp
RUN pip install pipenv && pipenv install --system

WORKDIR /app
ADD . /app/

# CMD ["./start.sh"]
