FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/* 
     
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app
COPY . /app

COPY --chown=1000:1000 . /app

COPY . .

EXPOSE 8000

CMD ["bash", "-c", "poetry run alembic upgrade head && poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]


