# PTT-Corpus/web

Web interface for PTTCorp

## Environment

Python > 3.6

## Development

### Environment variables

Please add these evvironment variables: 

    SECRET_KEY=
    MYSQL_HOST=
    MYSQL_PORT=
    MYSQL_USER=
    MYSQL_PASSWORD=
    MYSQL_DATABASE=
    ALLOWED_HOSTS=


### Install deppendencies

    pip install -r requirements/prod.txt 

### Deploy 

    python manage.py runserver
