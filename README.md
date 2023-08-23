# Foodgram
    https://foodgram41.ddns.net/
     
### Описание:
Cайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Технологии:
Python 3.10
Django 4.2
DRF 3.14
PostgreSQL
Docker
Gunicorn
Nginx
Djoser
Yandex Cloud
React

### Запуск проекта на сервере:
- Клонируйте репозиторий:
    ```
   SSH: git clone git@github.com:Snork41/foodgram-project-react.git
   HTTPS: git@github.com:Snork41/foodgram-project-react.git
    ```
- Создайте на сервере директорию __docs__ и скопируйте в нее файлы: _redoc.html_, _openapi-schema.yml_ из папки docs.
```
    scp <имя_файла> <username>@<IP>:/home/<username>/docs/
    # username - имя пользователя на сервере
    # IP - публичный IP сервера
```
- Создайте на сервере директорию __foodgram__ и скопируйте в нее файл _docker-compose.production.yml_ из папки infra.
- В директории __foodgram__ создайте файл __.env__, и заполните его:
```
SECRET_KEY='ваш_секретный_ключ'
ALLOWED_HOSTS='ваши_хосты_через_запятую_без_пробелов' или '*'
DEBUG=False
POSTGRES_USER=postgres
POSTGRES_PASSWORD='ваш_пароль_от_БД'
POSTGRES_DB=foodgram
DB_HOST=db
DB_PORT=5432
```
- Выполните поочерёдно команды на сервере для установки Docker и Docker Compose для Linux:
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin 
```
- Запустите docker compose:
```
sudo docker compose -f docker-compose.production.yml up -d
```
- Выполните миграции:
```
docker-compose exec backend python manage.py migrate
```
- Создайте админа:
```
docker-compose exec backend python manage.py createsuperuser
```
- Соберите статику:
```
docker-compose exec backend python manage.py collectstatic
```
- По желанию можете заполнить базу данных готовыми ингредиентами:
```
docker-compose exec backend python manage.py bd_load
```

##### __Документация API__ доступна по адресу:
https://foodgram41.ddns.net/api/docs/

---
#### Автор проекта:
- [Максим Давлеев](https://github.com/Snork41)