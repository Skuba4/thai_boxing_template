# Thai Boxing Template

> 🟢 Демо: [https://devarena.ru/](https://devarena.ru/)

---

**Thai Boxing Template** — основа для будущей полноценной платформы судейства.  
В дальнейшем планируется:
- расширенный интерфейс на React;
- продвинутая логика подсчёта очков;
- поддержка турниров и статистики;
- авторизация через соцсети;
- подача заявок на участие.

Проект демонстрирует ключевой функционал системы судейства и станет фундаментом для дальнейшего расширения.

---

## ⚙️ Функциональность проекта

### Упрощённая регистрация пользователей
Быстрая регистрация без личного кабинета.

### Роли пользователей

| Роль              | Функции                                                           |
|-------------------|--------------------------------------------------------------------|
| **Главный судья** | Создание комнат и пар, управление судьями, выбор победителя       |
| **Боковой судья** | Отправка записок, выставление оценок                              |
| **Наблюдатель**   | Просмотр боёв и оценок                                             |

---

## 💻 Stack

- Python 3.x  
- Django (Templates)  
- PostgreSQL  
- Docker & Docker Compose  
- Nginx  
- Vanilla JS + AJAX  
- HTML / CSS  

---

## 🛠 Tooling

- PyTest (unit & integration tests)  
- Certbot (SSL для продакшена)

---

## 💡 Особенности проекта

- Минималистичный фронтенд на Django Templates  
  _(в планах — переход на React)_
- Ролевая модель и mixins для разграничения прав
- Оптимизированные запросы и бизнес-логика:
  - предзагрузка связанных моделей
- Продуманная структура моделей:
  - `Rooms`, `Fights`, `Notes`
- Полноценные PyTest-тесты:
  - fixtures, unit, integration
- Docker-окружение для dev и prod

---

## ⚡ Установка (локалка TL;DR)

| Шаг | Команда / Действие                                                                                                                                |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Установи [Git](https://git-scm.com), [Docker](https://www.docker.com/products/docker-desktop), [PostgreSQL](https://www.postgresql.org/download/) |
| 2   | `git clone https://github.com/Skuba4/thai-boxing-template.git`                                                                                    |
| 3   | `cd thai-boxing-template`                                                                                                                          |
| 4   | Создай файл `.env` на основе `env.example`                                                                        |
| 5   | В `docker-compose.yml` закомментируй `nginx` (prod) и раскомментируй `nginx` (dev)                                                                 |
| 6   | `docker-compose up --build -d`                                                                                                                     |
| 7   | Открывай [http://localhost/](http://localhost/)                                                                                                    |

---

## 🗂 Файл `env.example`

В проекте лежит `env.example` — он содержит все нужные переменные окружения.  
Создай из него `.env`, отредактируй ключи и доступы — и можно запускать.

---

## 📦 Docker-шпаргалка

```bash
docker-compose up --build -d             # Запуск с пересборкой и в фоне
docker-compose stop                      # Остановить проект
docker-compose down -v --remove-orphans  # Полная очистка (контейнеры + volume)
docker-compose logs web                  # Логи Django-контейнера
docker-compose logs db                   # Логи PostgreSQL
docker-compose exec web sh               # Зайти внутрь контейнера
docker-compose build                     # Пересборка без запуска
