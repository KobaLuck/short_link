YaCut — сервис укорачивания ссылок и асинхронной загрузки файлов на Яндекс.Диск.

Возможности:
- генерация коротких ссылок и редирект на оригинальные URL;
- REST API для создания/получения ссылок (`/api/id/`, `/api/id/<short_id>/`);
- загрузка нескольких файлов на Я.Диск с получением ссылок для скачивания (страница `/files`);
- валидация пользовательских `custom_id` (длина ≤ 16, только [A-Za-z0-9]);
- автогенерация уникального 6-символьного идентификатора.

Требования:
- Python 3.9+
- Переменные окружения: `DATABASE_URI`, `SECRET_KEY`, `DISK_TOKEN` (для Я.Диска).

Клонировать репозиторий и перейти в него в командной строке:

```
git clone <URL-репозитория>
```

```
cd yacut-master
```

Создать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас Windows (Git Bash)

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt

Запуск приложения (локально):

```
flask --app yacut run
```

Переменные окружения (пример .env):

```
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=dev_secret_key
DISK_TOKEN=<ваш_oauth_токен_яндекс_диска>
```

API:
- POST `/api/id/`
  - тело: `{ "url": "https://example.com", "custom_id": "myid" }` (необязательно `custom_id`)
  - успех 201: `{ "url": "...", "short_link": "http://localhost/myid" }`
- GET `/api/id/<short_id>/`
  - успех 200: `{ "url": "..." }`

Документация:
- Архитектурный обзор: `docs/ARCHITECTURE.md`
- Спецификация: `openapi.yml` (можно открыть в Swagger Editor)
- Postman-коллекция: `postman_collection/Yacut.postman_collection.json`
```
