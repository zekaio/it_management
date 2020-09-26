#! /bin/bash
source env/bin/activate
gunicorn -c gunicorn_conf.py -b 127.0.0.1:5000 app:"create_app('development')"