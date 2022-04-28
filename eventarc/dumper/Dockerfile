FROM python:3.10-slim-bullseye

ENV POETRY_NO_INTERACTION=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

RUN pip install poetry

COPY poetry.toml /app/
COPY poetry.lock /app/
COPY pyproject.toml /app/
RUN poetry install --no-dev

COPY . /app

CMD ["sh", "-c", "poetry run waitress-serve --host 0.0.0.0 --port $PORT main:app"]
