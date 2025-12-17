# Multi-stage build for Backend (Python/FastAPI)
FROM python:3.12.10-slim AS backend-builder

ENV TZ=America/Manaus

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /tinto_api

COPY src/tinto_api/pyproject.toml src/tinto_api/poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY src/tinto_api ./

FROM node:24-alpine AS frontend-builder

WORKDIR /app

COPY src/web/package.json src/web/package-lock.json* src/web/yarn.lock* src/web/pnpm-lock.yaml* ./

RUN npm ci

COPY src/web ./

RUN npm run build

FROM python:3.12.10-slim AS backend

ENV TZ=America/Manaus

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /tinto_api

COPY src/tinto_api/pyproject.toml src/tinto_api/poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY src/tinto_api ./

EXPOSE 7777 6543

CMD ["poetry", "run", "task", "dev"]

FROM node:24-alpine AS frontend

WORKDIR /app

COPY src/web/package.json src/web/package-lock.json* src/web/yarn.lock* src/web/pnpm-lock.yaml* ./

RUN npm ci

COPY src/web ./

RUN npm run build

COPY --from=frontend-builder /app/.nuxt ./.nuxt
COPY --from=frontend-builder /app/.output ./.output

EXPOSE 3000

CMD ["npm", "run", "preview"]
