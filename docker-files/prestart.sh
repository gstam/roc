#! /usr/bin/env sh
echo "${0}: running makemigrations."
python /roc/manage.py makemigrations

echo "${0}: running migrations."
python /roc/manage.py migrate --noinput

echo "${0}: collecting statics."
python /roc/manage.py collectstatic --noinput
