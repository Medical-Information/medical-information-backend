# medical-information-backend

## Развертывание в режиме разработчика
### Клонировать репозиторий
```
git clone git@github.com:Medical-Information/medical-information-backend.git
```
### Создать виртуальное окружение
```
python3.11 -n venv venv
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
| USE_SQLITE | True | Использовать SQLite вместо PostgreSQL |
| POSTGRES_DB | postgres | Имя базы данных |
| POSTGRES_USER | postgres | Имя пользователя (владельца) базы данных |
| POSTGRES_PASSWORD | postgres | Пароль пользователя (владельца) базы данных |
| POSTGRES_HOST | 127.0.0.1 | ip-адрес хоста, на котором находится база данных |
| POSTGRES_PORT | 5432 | порт, который слушает база данных |
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
- Открыть страницу документации API [localhost:8000/api/v1/swagger/](http://localhost:8000/api/v1/swagger/)
### Установка pre-commit хуков
```
pre-commit install
```
