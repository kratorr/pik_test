# Тестовое задание ПИК.ПРО

Cервис для ведения учёта положенных в доме кирпичей.

# Как установить


Для работы необоходим Python 3. 
Установите зависимости с помощью pip:
```bash
pip install -r requirements.txt
```
Для лучшей изоляции  рекомендуется использовать виртуальное окружение.

# Quickstart


Запуск на встроенном сервере Django
```bash
$ python3 manage.py runserver
```

# Как использовать

## Создать здание

### Request

`POST /api/building/`

    curl  -X POST  http://localhost:8000/api/building/  -H 'Content-Type: application/json' -d '{"construction_year":2000,"address":"Москва, ул.Пушкина д. 1"}'

## Положить N кирпичей в дом с id в момент времени T.

### Request

`POST /building/{id}/add-bricks/`

    curl  -X POST  http://localhost:8000/api/building/1/add-bricks/  -H 'Content-Type: application/json' -d '{"count": 1000, "date":"2020-03-21"}'

## Получить  статистику по всем существующим домам - сколько в каждом лежит кирпичей с группировкой по датам

### Request

`GET /api/stats/`

    curl  -X GET  http://localhost:8000/api/stats/

