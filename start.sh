#!/usr/bin/env sh
python manage.py collectstatic --no-input  && \
uwsgi --master --http 0.0.0.0:8888 --module web.wsgi --static-map /static_pttweb=static_pttweb --process 4 --manage-script-name --mount=/_pttcorp=web/wsgi.py
