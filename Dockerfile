# STAGE 1: Builder

FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-interaction --no-ansi --only main

# STAGE 2: Runner

FROM python:3.11-slim as runner 

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

EXPOSE 8000

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]


