# Этап сборки (builder)
FROM python:3.10-slim AS builder

WORKDIR /app

# Установка системных библиотек, необходимых для сборки cryptography
# cryptography - библиотека которая нужна для работы тома mysql.
# остальные зависимости, по типу gcc (компилятор С для питона) нужны для Ubuntu, на котором работает наш контейнер
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/* 
     
# Установка Poetry
RUN pip install --no-cache-dir poetry
# Оптимизация с помощью --no-cache-dir, чтобы избежать сохранения кеша
# Также обьединение в одну команду RUN

# Копирование файлов для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей с помощью Poetry
# config virtualenvs.create true - создает вирт. окр. среду для выполнения poetry в консоли docker тоже в env, как мы это используем прямо сейчас
# по другому оно работать не будет - будет выдавать ошибку что библиотек не существует, потому-что вирт. окружение не было создано. (по сути это аналог команды poetry shell для докера)
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Финальный образ  (Первый этап сборки (builder) устанавливает все зависимости и сохраняет их в виртуальном окружении. На финальном этапе только необходимые файлы копируются в финальный образ, без установленных компиляторов и библиотек.)

FROM python:3.10-slim

WORKDIR /app
# Копирование зависимостей из builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app
COPY . /app

# --chown=1000:1000 - специальный паараметр команды который добавляет расширения для докер-файлов чтобы их нормально распознала винда
# однако, ее можно будет даже и не использовать (я гляну позже)
COPY --chown=1000:1000 . /app


# Копирование приложения
COPY . .

EXPOSE 8000

# CMD ["bash", "-c", "\
#     if ! poetry run python -c 'import uvicorn' &>/dev/null; then \
#         echo 'Virtual environment seems broken. Reinstalling dependencies...'; \
#         poetry install --no-root; \
#     fi; \
#     poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]


CMD ["bash", "-c", "poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]

