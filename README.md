# SpendWise — Dockerized Expense Tracker

A simple real-life web project for tracking personal expenses.

## Tech Stack

- Frontend: HTML + CSS
- Backend: Python Flask
- Database: PostgreSQL
- Containerization: Docker
- Orchestration: Docker Compose
- Production server: Gunicorn

## Architecture

Browser → Flask/Gunicorn container → PostgreSQL container

## Run

```bash
docker compose up -d --build
```

Open:

http://localhost:8080

Health check:

http://localhost:8080/health

Stop:

```bash
docker compose down
```

Stop and delete database volume:

```bash
docker compose down -v
```

## Git

```bash
git add .
git commit -m "feat: add dockerized expense tracker"
git push origin main
```
