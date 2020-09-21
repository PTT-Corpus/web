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

### Before executing `docker-compose`...

Please first export INDEX_PATH to the right path of blacklab index.
E.g.
```
$ export INDEX_PATH=~/blacklab_index
```



### Install deppendencies

    pip install -r requirements/prod.txt 

### Deploy 


For development:

    python manage.py runserver

For production:

    uwsgi --master --http 0.0.0.0:8888 --module web.wsgi --static-map /static_pttweb=static_pttweb --process 4 --manage-script-name --mount=/_pttcorp=web/wsgi.py
