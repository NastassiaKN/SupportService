# Support Service — Ticket System

A web-based ticket management system developed as a diploma project.

The system allows users to create support tickets, communicate with support managers, and track issue resolution.  
Support managers handle tickets with automatic workload balancing.

---

## Project Overview

This project is built using Django and follows a modular architecture with two main applications:

- `accounts` — user authentication and role management  
- `helpdesk` — ticket management system and business logic  

The system includes an automatic ticket assignment mechanism based on workload.

---

## Features

### User:

- create support tickets  
- add ticket description  
- upload attachments
- send messages in ticket chat
- view own tickets
- close ticket
- confirm issue resolution

### Support manager:

- view assigned tickets  
- update ticket status  
- set priority  
- communicate with users (messages)  
- upload attachments  
- filter tickets (status, priority, creation date)

### Admin:

- full system management via Django admin  
- monitor all tickets  
- assign tickets to support managers  
- manage users and groups  
- update ticket status and priority  
- communicate in tickets  
- filter tickets by status, priority, manager, creation date  

### Auto-assignment:

- tickets are automatically assigned to the least loaded manager  
- load is calculated based on tickets with **new** and **in progress** status  
- if a manager creates a ticket, it is automatically assigned to them  

---

## Tech Stack

- Python 3  
- Django  
- SQLite  
- HTML / CSS  
- Docker  

---

## Architecture

The project is built using the **MVT (Model-View-Template)** architecture:

- Model — database layer  
- View — business logic  
- Template — UI  

---

## Project Structure

### Applications

- `accounts/` — authentication, authorization, user roles  
- `helpdesk/` — ticket system, messaging, business logic  

### Core files

- `manage.py` — Django project entry point  
- `requirements.txt` — project dependencies  
- `Dockerfile` — Docker image configuration  
- `docker-compose.yml` — container orchestration  
- `.env` — environment variables (excluded from repository)

---

## Security

- sensitive data is stored in `.env`  
- `.env` is excluded from the repository  
- database file (`db.sqlite3`) is not tracked by Git  
- uploaded files (`attachments`) are not stored in the repository  

---

## Running with Docker

### 1. Clone repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create .env file

```
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Build and run containers

```
docker-compose up --build
```

### 4. Open application in browser

```
http://localhost:8000
```

---

## Running without Docker

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Working with Database

```
python manage.py migrate
python manage.py createsuperuser
```

---

## Purpose of the project

This project was developed as part of a diploma and demonstrates:

- backend development using Django
- user authentication and role-based access control
- file upload handling
- ticket workflow simulation
- automated workload balancing algorithm
- containerization using Docker





