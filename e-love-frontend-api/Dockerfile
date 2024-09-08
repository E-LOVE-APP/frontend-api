FROM python:3.10-slim

WORKDIR /app

# Установка системных библиотек, необходимых для сборки cryptography
# cryptography - библиотека которая нужна для работы тома mysql.
# остальные зависимости, по типу gcc (компилятор С для питона) нужны для Ubuntu, на котором работает наш контейнер
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

# Установка зависимостей с помощью Poetry
# config virtualenvs.create true - создает вирт. окр. среду для выполнения poetry в консоли docker тоже в env, как мы это используем прямо сейчас
# по другому оно работать не будет - будет выдавать ошибку что библиотек не существует, потому-что вирт. окружение не было создано. (по сути это аналог команды poetry shell для докера)
RUN poetry config virtualenvs.create true && poetry install --no-root

# --chown=1000:1000 - специальный паараметр команды который добавляет расширения для докер-файлов чтобы их нормально распознала винда
# однако, ее можно будет даже и не использовать (я гляну позже)
COPY --chown=1000:1000 . /app

EXPOSE 8000

# Запуск сервера
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
