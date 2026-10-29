# YaCut · короткие ссылки

Сервис коротких ссылок с REST API и асинхронной загрузкой файлов на Яндекс.Диск.

**Python · Flask · SQLAlchemy · aiohttp**

## Быстрый старт

```bash
git clone https://github.com/KobaLuck/short_link.git
cd short_link
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
flask --app yacut shell
# В открывшейсяся оболочке: from yacut import db; db.create_all()
# Затем exit()
flask --app yacut run
```

В Windows PowerShell окружение активируется командой `.venv\Scripts\Activate.ps1`.

Создайте `.env`: `DATABASE_URI=sqlite:///db.sqlite3`, случайный `SECRET_KEY` и `DISK_TOKEN` для загрузки файлов. Произвольный идентификатор: до 16 латинских букв и цифр. Без него генерируется 6 символов. Страница загрузки: `/files`.

## API и документация

- `POST /api/id/` — создать ссылку: `{"url": "https://example.com", "custom_id": "demo"}`.
- `GET /api/id/<short_id>/` — получить исходный адрес.
- [Архитектура](docs/ARCHITECTURE.md) · [OpenAPI](openapi.yml) · [Postman](postman_collection/README.md).

## Структура

- `tests/` — автоматические проверки.
- `docs/` — документация.
- `postman_collection/` — коллекции запросов.

## Проверки

```bash
python -m pytest
```

---

[Никита Казанцев](https://github.com/KobaLuck) · [Все публичные проекты](https://github.com/KobaLuck?tab=repositories)
