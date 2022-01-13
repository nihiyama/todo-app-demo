#!/bin/sh

# connect db
PYTHONPATH=. python app/pre_start.py

# db migrate
PYTHONPATH=. alembic upgrade head

# create superuser
PYTHONPATH=. python app/create_superuser.py

# start app
if [ $APP_ENV = "development" ]; then
    PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --reload --log-config /opt/app/uvicorn_log_config.yml
elif [ $APP_ENV = "production" ]; then
    PYTHONPATH=. gunicorn -k uvicorn.workers.UvicornWorker -c /opt/app/gunicorn_conf.py app.main:app
else
    echo "Choose development or production"
fi