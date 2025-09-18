#!/bin/sh

# Ожидаем БД
echo "Ожидаем PostgreSQL на $DB_HOST:$DB_PORT..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL доступна!"

# Применяем миграции
python manage.py migrate --noinput

exec "$@"
