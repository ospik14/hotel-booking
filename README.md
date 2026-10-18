# Hotel Booking API

Backend для бронювання готельних номерів на FastAPI + SQLAlchemy 2 (async) + PostgreSQL.

## Стек

- Python 3.12
- FastAPI / Pydantic v2
- SQLAlchemy 2.0 + AsyncSession
- PostgreSQL + Alembic
- JWT (python-jose) + Argon2

## Швидкий старт

### 1. Залежності

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Змінні середовища

Скопіюйте `.env.example` у `.env` і задайте значення:

```bash
cp .env.example .env
```

Обов’язкові змінні:

- `DATABASE_URL` — наприклад `postgresql+asyncpg://postgres:password@localhost:5432/mrb`
- `SECRET_KEY` — довгий випадковий рядок
- `ALGORITHM` — зазвичай `HS256`

### 3. PostgreSQL

```bash
docker compose up -d
```

### 4. Міграції

```bash
alembic upgrade head
```

### 5. Адміністратор

Публічна реєстрація завжди створює користувача з роллю `user`. Адміна створюйте скриптом:

```bash
PYTHONPATH=src python -m scripts.create_admin \
  --email admin@example.com \
  --password 'StrongPass1' \
  --first-name Admin \
  --last-name User
```

### 6. Запуск API

```bash
PYTHONPATH=src uvicorn main:app --reload --app-dir src
```

Документація: `http://localhost:8000/docs`

### 7. Тести

Потрібен запущений PostgreSQL з застосованими міграціями.

```bash
pytest -q
```

## Основні endpoint-и

| Метод | Шлях | Доступ | Опис |
|-------|------|--------|------|
| POST | `/users/register` | public | Реєстрація |
| POST | `/users/login` | public | JWT логін |
| GET/PATCH | `/users/me/` | user | Профіль |
| POST | `/users/change-password/` | user | Зміна пароля |
| POST | `/rooms/` | admin | Створити номер |
| GET | `/rooms/` | public | Список / фільтри |
| GET | `/rooms/available/` | public | Вільні номери на дати |
| GET | `/rooms/{id}/` | user | Деталі номера |
| PATCH | `/rooms/{id}/` | admin | Оновлення |
| DELETE | `/rooms/{id}/` | admin | Деактивація (`is_active=false`) |
| POST | `/booking/` | user | Створити бронювання |
| GET | `/booking/my/` | user | Мої бронювання |
| GET | `/booking/` | admin | Усі бронювання |
| GET | `/booking/{id}/` | user/admin | Деталі |
| DELETE | `/booking/{id}/` | user/admin | Скасування (soft) |
| PATCH | `/booking/{id}/status/` | admin | Зміна статусу |

## Бізнес-правила бронювання

- Інтервал зайнятості: `[check_in, check_out)` — день виїзду вільний для наступного гостя.
- Конкурентна безпека: `SELECT FOR UPDATE` на номері + PostgreSQL `EXCLUDE` constraint для `CONFIRMED`.
- Вартість = ночі × `price_per_night` номера на момент створення; зберігається snapshot у бронюванні.
- Скасування не видаляє запис — статус `CANCELLED`.
