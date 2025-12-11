FROM node:24-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

RUN npm ci

COPY . .

RUN npm run build

FROM node:24-alpine

WORKDIR /app

COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

RUN npm ci

COPY . .

RUN npm run build

COPY --from=builder /app/.nuxt ./.nuxt
COPY --from=builder /app/.output ./.output

EXPOSE 3000

CMD ["npm", "run", "preview"]