FROM python:3.12-slim
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# дать права и сделать entrypoint исполняемым (root)
RUN chmod +x /app/entrypoint.sh
# создаем нового пользователя для работы внутри (безопасность)
RUN useradd -m app && chown -R app:app /app

# переключаемся на пользователя app
USER app
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "boxing.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "5"]
