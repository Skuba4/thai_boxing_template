#!/bin/sh

# Ожидание готовности БД
echo "Ожидаем PostgreSQL на $DB_HOST:$DB_PORT..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL доступна!"

# Миграции
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Запуск Gunicorn
exec gunicorn boxing.wsgi:application --bind 0.0.0.0:8000
