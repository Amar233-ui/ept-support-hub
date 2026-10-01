# syntax=docker/dockerfile:1

# ---------- dev: Vite dev server with HMR on mounted sources ----------
FROM node:24-alpine AS dev
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY . .
EXPOSE 5173
HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=5 \
  CMD wget -qO- http://127.0.0.1:5173/ >/dev/null || exit 1
# node_modules lives in a named volume: reinstall when package-lock changes, then start.
CMD ["sh", "-c", "npm ci --no-audit --no-fund --prefer-offline && npm run dev"]

# ---------- build ----------
FROM node:24-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY . .
RUN npm run build

# ---------- prod: static files served by unprivileged Nginx ----------
FROM nginxinc/nginx-unprivileged:1.31-alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --retries=5 \
  CMD wget -qO- http://127.0.0.1:8080/ >/dev/null || exit 1
