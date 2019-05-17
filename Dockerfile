FROM python:3.6.6-alpine3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD . /app/
RUN apk update && apk add python3-dev build-base linux-headers pcre-dev mariadb-dev 
RUN pip install pipenv && pipenv install --system
# CMD ["./start.sh"]
