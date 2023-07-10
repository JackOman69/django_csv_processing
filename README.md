<h1>Сервис по анализу CSV файлов</h1>

---

## Инструментарий проекта:

* `Python 3.10.7`
* `Gunicorn`
* `Django`
* `Django Rest Framework`
* `PostgreSQL`
* `Psycopg2`
* `Pandas`
* `Redis`
* `Django-Redis`
* `Channels-Redis`
* `Dotenv`
* `Whitenoise`
* `Docker (Compose)`

---
## Директория проекта:

```
django_csv_processing/
│   README.md
│   docker-compose.yml
|   Dockerfile
|   manage.py
|   .env
|   .gitignore
|   requirements.txt   
│
└───processing/
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   models.py
|   |   serializer.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   |
│   └───migrations/
|   |   |   __init__.py
|   |   |   0001_initial.py   
|   |   |
└───postgres/
|   │   Dockerfile
|   |   
└───persistentdata/
|   |
|   └───media/
|   |   README.md
|   |  
|   └───static/
|   |   README.md
|   |    
└───csvprocessing/
|   |   __init__.py
|   |   asgi.py
|   |   local_settings.py
|   |   settings.py
|   |   urls.py
|   |   wsgi.py
|   |
```

---

## Установка:

### Первичная инициализация проекта:

```console
$ git clone https://github.com/JackOman69/voice_stickers_telegram.git
```
<a href="https://docs.docker.com/desktop/">Docker Desktop</a>

### Установка .env:
# В проекте уже имеются файлы .env и local_settings.py
* Создайте файл `.env` в корневой директории и вложите туда переменную Django key:

```python
DJANGO_SECRET_KEY = "ВАШ_СЕКРЕТНЫЙ_КЛЮЧ_ПРОЕКТА"
```

### Установка local_settings.py:

* Создайте файл `local_settings.py` в папке `csvprocessing` и вложите туда следующие настройки:

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],  # or [("redis", 6379)] in docker
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_db',
        'USER': 'django',
        'PASSWORD': 'djingo',
        # 'HOST': 'postgresql', # FOr docker
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'DISABLE_SERVER_SIDE_CURSORS': True
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://redis:6379/1", # For docker
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

---

## Запуск

### Запуск docker-а:

* Запускать проект нужно с помощью следующей команды:

```console
$ docker-compose up --build
``` 

---

## Проверка:

* Проверка работоспособности проекта осуществляется переходом на http://127.0.0.1:8008/api/ или http://127.0.0.1:8008/admin/
* Если хотите проверить админ панель, то внутри консоли контейнера Django запустите команду `python manage.py createsuperuser` и создайте администратора для Django админ панели

### Запросы:

- `POST http://127.0.0.1:8008/csv/process/` - Запрос на вложение csv файла в сервер
Запрос осуществляется с помощью `Multipart Form` и ключа `deals`
- Ответ HTTP_200:
```json
{
	"Status": "OK"
}
```
- Ответ HTTP_400:
```json
{
	"Status": "Error",
	"Desc": "Неподдерживаемый формат файла - в процессе обработки файла произошла ошибка"
}
```
- Ответ HTTP_400 с любым другим видом ошибки:
```json
{
	"Status": "Error",
	"Desc": "{Error} - в процессе обработки файла произошла ошибка"
}
```

- `GET http://127.0.0.1:8008/csv/process/` - Запрос на получение данных с последнего закаченного csv файла на сервер
- Ответ HTTP_200:
```json
{
	"response": [
		{
			"username": "resplendent",
			"spent_money": 451731,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		},
		{
			"username": "bellwether",
			"spent_money": 217794,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		},
		{
			"username": "uvulaperfly117",
			"spent_money": 120419,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		},
		{
			"username": "braggadocio",
			"spent_money": 108957,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		},
		{
			"username": "turophile",
			"spent_money": 100132,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		}
	]
}
```

- `GET http://127.0.0.1:8008/csv/get_csv/<int:id>` - Запрос на получение данных с csv файла по его ID
- Ответ HTTP_200:
```json
{
	"response": [
		{
			"username": "resplendent",
			"spent_money": 451731,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		},
		{
			"username": "bellwether",
			"spent_money": 217794,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		},
		{
			"username": "uvulaperfly117",
			"spent_money": 120419,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		},
		{
			"username": "braggadocio",
			"spent_money": 108957,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		},
		{
			"username": "turophile",
			"spent_money": 100132,
			"gems": [
				"Сапфир",
				"Танзанит"
			]
		}
	]
}
```

**Все GET запросы кешируются с помощью Redis на 15 минут**