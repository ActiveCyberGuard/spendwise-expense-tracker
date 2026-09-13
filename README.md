# 💰 SpendWise — Dockerized Expense Tracker

A simple real-life web application for tracking and managing personal expenses.

SpendWise allows users to add, view, categorize, and delete daily expenses through a web interface backed by PostgreSQL.

---

## ✨ Features

* Add personal expenses
* View all expenses
* Delete expenses
* Category-wise expense summary
* Total expense calculation
* PostgreSQL database storage
* Health check endpoint
* Dockerized application
* Multi-container setup using Docker Compose

---

## 🛠️ Tech Stack

* **Frontend:** HTML + CSS
* **Backend:** Python Flask
* **Database:** PostgreSQL
* **Containerization:** Docker
* **Orchestration:** Docker Compose
* **Production Server:** Gunicorn
* **Version Control:** Git + GitHub

---

## 🏗️ Architecture

```text
┌──────────────────┐
│   Web Browser    │
│ localhost:8080   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   expense-web    │
│ Flask + Gunicorn │
│    Port 5000     │
└────────┬─────────┘
         │
         │ Docker Network
         ▼
┌──────────────────┐
│    expense-db    │
│    PostgreSQL    │
│    Port 5432     │
└──────────────────┘
```

---

## 📁 Project Structure

```text
expense-tracker-docker/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

---

# 🚀 Run the Project

## 1. Clone the Repository

```bash
git clone https://github.com/ActiveCyberGuard/spendwise-expense-tracker.git
```

Move into the project:

```bash
cd spendwise-expense-tracker/expense-tracker-docker
```

---

## 2. Build and Start Containers

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker ps
```

You should see:

```text
expense-web
expense-db
```

---

## 🌐 Open the Application

Open your browser:

```text
http://localhost:8080
```

---

## ❤️ Health Check

Check application and database connectivity:

```text
http://localhost:8080/health
```

Expected response:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

# 🗄️ Database

Connect to PostgreSQL:

```bash
docker exec -it expense-db psql -U expenseuser -d expenses
```

Show tables:

```sql
\dt
```

View expenses:

```sql
SELECT * FROM expenses;
```

Exit:

```sql
\q
```

---

# 🐳 Docker Commands

### Start

```bash
docker compose up -d
```

### Build and Start

```bash
docker compose up -d --build
```

### View Containers

```bash
docker ps
```

### View Web Logs

```bash
docker logs expense-web
```

### View Database Logs

```bash
docker logs expense-db
```

### Stop Containers

```bash
docker compose down
```

### Stop and Delete Database Volume

```bash
docker compose down -v
```

> ⚠️ `docker compose down -v` removes the PostgreSQL volume and deletes stored database data.

---

# 🧪 Testing

The application was tested for:

* Adding expenses
* Viewing expenses
* Deleting expenses
* Category-wise expense calculation
* PostgreSQL database connectivity
* Docker container communication
* Health check endpoint

---
 
---

# 🔄 Development Workflow

```text
Develop Application
        ↓
Create Dockerfile
        ↓
Build Docker Image
        ↓
Docker Compose
        ↓
Start Web + Database Containers
        ↓
Test Application
        ↓
Git Add
        ↓
Git Commit
        ↓
Git Push
        ↓
GitHub
```

---

# 📌 Project Objective

The main objective of this project is to demonstrate how a real-life web application can be containerized and deployed using Docker and Docker Compose.

The project demonstrates:

* Web application development
* Docker image creation
* Dockerfile usage
* Docker container creation
* Docker Compose
* PostgreSQL integration
* Container networking
* Database persistence
* Application health checking
* Git and GitHub workflow

---

# 👨‍💻 Author

**MD.AL-AMIN**

BSc in Information & Communication Technology
Jahangirnagar University

GitHub: **ActiveCyberGuard**

---

## 📄 License

This project is created for educational and internship purposes.
