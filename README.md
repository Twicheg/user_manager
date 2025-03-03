# Сервис для хранения данных о пользователях


### Описание
BackEnd часть 

Реализовать RestAPI сервис, который позволяет выполнить запрос в сторонний API (https://api.nationalize.io/?name=%D0%90%D1%80%D1%82%D0%B5%D0%BC).\
Должны быть реализованы как минимум 2 endpoint:\
    1. GET /names?name=Vadim\
        a. Выполняется запрос в БД или API и возвращается результат\
    2. POST /names со следующей нагрузкой:\
{\
  "count": 749,\
  "name": "Артем",\
  "country": [\
    {\
      "country_id": "RU",\
      "probability": 0.48747151850296\
    },\
    {\
      "country_id": "KZ",\
      "probability": 0.174757725611249\
    },\
    {\
      "country_id": "UA",\
      "probability": 0.0313840470957702\
    },\
    {\
      "country_id": "LT",\
      "probability": 0.00754926139580072\
    },\
    {\
      "country_id": "MD",\
      "probability": 0.00754926139580072\
    }
  ]
} \
        a. Данные сохраняются в БД\
Основные требования к системе:\
    1. Предусмотреть кэш хранилище для запросов в БД (опциональный этап)\
    2. Взаимодействие с БД должно быть построено через ORM (Django ORM, SQLAlchemy и др.)\
    3. В качестве БД можно использовать SQLite или PostgreSQL\
    4. В случае добавления новых данных по API система не должна выполнять запрос во внешний API.\
    5. Все endpoint должны проверять на корректность входные параметры и возвращать правильные status code.\
    6. Проект должен иметь в своем составе документацию (Файл ReadMe) в котором описывается алгоритм запуска, примененные алгоритмы и др.\
    7. В проекте должна быть выполнена документация Swagger (в виде отдельного endpoint)\
    8. Структура хранения данных в БД и иные не описанные в данном задании вещи, реализовываются по усмотрению кандидата и должны быть описаны в сопроводительной документации.\

FrontEnd
 
Реализовать пользовательский интерфейс на базе реализованного RestAPI. Пользовательский интерфейс, должен предусматривать возможность запросить данные в API и получить в наглядном представлении ответ.\
Интерфейс должен обращаться к RestAPI с помощью JS.\
В рамках данного задания не оценивается дизайнерская составляющая FrontEnd.

## Стек
- python3.13
- fastapi
- SQLAlchemy
- pydantic
- jinja2
- redis
- docker
- docker-compose

### Инструкции для запуска
варианты запуска:\
В папке проекта 
1. сделать билд `docker build . -t "user_service"` ,\
запуск приложения через `docker-compose up`\
создать файл .env с полями:\
DB_NAME= your_db_name\
REDIS=ON
REDIS_PORT=6379\
REDIS_HOST=redis

2. pip install -r requirements.txt  
fastapi run application/app.py --port 8000
в .env:
DB_NAME= your_db_name\
REDIS=ON\
REDIS_PORT=6379\
REDIS_HOST=localhost

### http://0.0.0.0:8000/documentation


### Api Эндпоинты
* GET 0.0.0.0:8000 - html page
* POST 0.0.0.0:8000/names - добавление нового пользователя http://0.0.0.0:8000/documentation#/user/create_user_names__post
* GET 0.0.0.0:8000/names - получение списка всех пользователей
* GET 0.0.0.0:8000/names/?name={имя} - поиск по имени в базе данных, если отсутствует - запрос к https://api.nationalize.io/?name={имя} и сохранение в базе данных

Запрос с html страницы происходит с помощью JS на путь, указанный в поле. JS код находиться в static/js/myJS.js
