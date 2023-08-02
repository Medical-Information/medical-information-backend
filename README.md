# medical-information-backend

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

## Развертывание в режиме разработчика
### Клонировать репозиторий
```
git clone git@github.com:Medical-Information/medical-information-backend.git
```
### Перейти в директорию medical-information-backend
```
cd medical-information-backend
```
### Создать виртуальное окружение
```
python3.11 -m venv venv
```
### Активировать виртуальное окружение
```
. ./venv/bin/activate
```
### Обновить установщик пакетов pip
```
pip install --upgrade pip
```
### Установить зависимости
```
pip install -r ./stethoscope/requirements/dev.txt
```
### В директории stethoscope скопировать файл `.env.example` в `.env` и задать значения переменным


| Переменная | Значение по умолчанию | Описание |
| --- | --- | --- |
| DEBUG | False | Режим отладки |
| SECRET_KEY | None | `from django.core.management.utils import get_random_secret_key; get_random_secret_key()` |
| ALLOWED_HOSTS | * | Список разрешенных хостов, указанных через пробел |
| POSTGRES_DB | postgres | Имя базы данных |
| POSTGRES_USER | postgres | Имя пользователя (владельца) базы данных |
| POSTGRES_PASSWORD | postgres | Пароль пользователя (владельца) базы данных |
| POSTGRES_HOST | 127.0.0.1 | ip-адрес хоста, на котором находится база данных |
| POSTGRES_PORT | 5432 | порт, который слушает база данных |
| EMAIL_HOST | *** | адрес smtp-сервера
| EMAIL_HOST_USER | *** | адрес электронной почты
| DEFAULT_FROM_EMAIL | *** | адрес электронной почты
| EMAIL_HOST_PASSWORD | *** | пароль к электронной почте
| EMAIL_PORT | *** | порт smtp-сервера |
| EMAIL_USE_SSL | True or False | True если формат шифрования SSL, тогда EMAIL_USE_TLS=False |
| EMAIL_USE_TLS | True or False | True если формат шифрования TLS, тогда EMAIL_USE_SSL=False |
| CURSOR_PAGINATION_PAGE_SIZE | 6 | Размер страницы пагинации по умолчанию |
| CURSOR_PAGINATION_MAX_PAGE_SIZE | 50 | Максимальный размер страницы пагинации |
| CELERY_BROKER | redis://localhost:6379/0 | URL брокера |
| URL_ARTICLES | http://localhost:8000/api/v1/articles/ | URL для получения статей |


### Перейти в директорию infra/dev/
```
cd infra/dev/
```
### Запустить контейнер с базой данных PostgreSQL
```
docker compose up -d
```
### Вернуться в директорию проекта
```
cd ../..
```
### Применить миграции
```
python manage.py migrate
```
### Создать суперпользователя
```
python manage.py createsuperuser
```
### Запустить сервер
```
python manage.py runserver
```
## Полезности
### Ссылки
- Открыть панель администратора [localhost:8000/admin/](http://localhost:8000/admin/)
- Открыть главную страницу [localhost:8000/](http://localhost:8000/)
- Открыть страницы документации API:
  * [api.yaml](https://stethoscope.acceleratorpracticum.ru/api/v1/schema/)
  * [swagger-ui](https://stethoscope.acceleratorpracticum.ru/api/v1/schema/swagger-ui/)
  * [redoc](https://stethoscope.acceleratorpracticum.ru/api/v1/schema/redoc/)
### Установка pre-commit хуков
```
pre-commit install
```

### Запросы к API
- Получить список всех пользователей/регистрация пользователя [localhost:8000/api/v1/users/](http://localhost:8000/api/v1/users/)
- Получить (изменить, удалить) информацию о себе [localhost:8000/api/v1/users/me/](http://localhost:8000/api/v1/users/me/)

- Активировать пользователя [localhost:8000/api/v1/users/activation/](localhost:8000/api/v1/users/activation/)
- Повторный запрос активации пользователя [localhost:8000/api/v1/users/resend_activation/](localhost:8000/api/v1/users/resend_activation/)
users/resend_activation/

- Изменения пароля пользователя [localhost:8000/api/v1/users/set_password/](http://localhost:8000/api/v1/users/set_password/)
- Сброс пароля [localhost:8000/api/v1/users/reset_password/](http://localhost:8000/api/v1/users/reset_password/)
- Подтверждение сброса пароля [localhost:8000/api/v1/users/reset_password_confirm/](http://localhost:8000/api/v1/users/reset_password_confirm/)

- Получить токен авторизации [localhost:8000/api/v1/auth/token/login/](http://localhost:8000/api/v1/auth/login/)
- Удалить токен авторизации [localhost:8000/api/v1/auth/token/logout/](http://localhost:8000/api/v1/auth/logout/)

- Поставить лайк статье [localhost:8000/api/v1/articles/<id_articles>/vote/like/](http://localhost:8000/api/v1/articles/<id_articles>/vote/like/)
- Поставить дизлайк статье [localhost:8000/api/v1/articles/<id_articles>/vote/dislike/](http://localhost:8000/api/v1/articles/<id_articles>/vote/dislike/)
- Удалить голос за статью [localhost:8000/api/v1/articles/<id_articles>/unvote/](http://localhost:8000/api/v1/articles/<id_articles>/unvote/)
- Получить список лайкнувших статью [localhost:8000/api/v1/articles/<id_articles>/votes/fans/](http://localhost:8000/api/v1/articles/<id_articles>/votes/fans/)
- Получить список дизлайкнувших статью [localhost:8000/api/v1/articles/<id_articles>/votes/haters/](http://localhost:8000/api/v1/articles/<id_articles>/votes/haters/)


Тестовый запуск дополнительных процессов:
- celery -A stethoscope worker                      # асинхронная очередь задач
- celery -A stethoscope beat                        # планировщик заданий
- celery -A stethoscope flower                      # мониторинг
- docker run -d -p 6379:6379 --name redis redis     # брокер сообщений
