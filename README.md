# 🚀 Simple FastAPI Application

This is a lightweight yet powerful **FastAPI** application designed with modern backend best practices in mind. 🧠💡

---

## 🔑 Key Features

1. 🐳 **Dockerization**  
   Easily containerized with Docker for consistent development and deployment across environments.  
   `docker-compose` friendly! 📦

2. 🚦 **Rate Limiting**  
   Protect your APIs from abuse using smart throttling mechanisms.  
   Keeps the bad bots out! 🤖❌

3. ⚡ **Redis Caching for DB Calls**  
   Improve performance by caching expensive database queries.  
   Super fast, super efficient! 🧠💾

4. 🐘 **PostgreSQL (via psycopg2)**  
   Rock-solid relational database integration using the battle-tested `psycopg2` driver.  
   Structured storage you can rely on. 📊

5. 🐞 **Logging for Debugging**  
   Stay on top of what's happening in your app with clean, configurable logging.  
   `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` — we've got it all! 📋🔍

6. 🔀 **Routing**  
   Organized, clean, and modular routing to scale your app with ease.  
   One endpoint at a time! 🛣️

7. 🛡️ **Pydantic Validation for POST Data**  
   Ensure your input data is correct using `Pydantic` models.  
   Say goodbye to unexpected bugs! ✅🐍

---

## 📦 Tech Stack

| Tool / Tech     | Logo / Emoji |
|-----------------|--------------|
| **FastAPI**     | ⚡ ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white&style=flat) |
| **Docker**      | 🐳 ![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white&style=flat) |
| **PostgreSQL**  | 🐘 ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?logo=postgresql&logoColor=white&style=flat) |
| **Redis**       | 🚀 ![Redis](https://img.shields.io/badge/-Redis-DC382D?logo=redis&logoColor=white&style=flat) |
| **Pydantic**    | 🛡️ ![Pydantic](https://img.shields.io/badge/-Pydantic-0A66C2?logo=python&logoColor=white&style=flat) |
| **psycopg2**    | 🔌 ![Python](https://img.shields.io/badge/-psycopg2-3776AB?logo=python&logoColor=white&style=flat) |
| **Logging**     | 📋 ![Log](https://img.shields.io/badge/-Logging-000000?logo=logstash&logoColor=white&style=flat) |

> 🎯 This template is perfect for those starting with FastAPI or building scalable backend services with modern features built-in!

---

## 📁 Project Structure

```bash
.
├── LICENSE
├── docker-compose.yaml
├── init.sql
├── logs
│   ├── app.log
│   ├── database.log
│   ├── items_route.log
│   └── user_route.log
└── src
    ├── Dockerfile
    ├── app.py
    ├── database
    │   ├── core.py
    │   ├── items.py
    │   └── users.py
    ├── log_util.py
    ├── requirements.txt
    └── route
        ├── items.py
        └── users.py

5 directories, 16 files
