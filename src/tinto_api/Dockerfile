FROM python:3.12.10-slim

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adicionar Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /tinto_api

COPY pyproject.toml poetry.lock ./

COPY README.md ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "task", "run"]