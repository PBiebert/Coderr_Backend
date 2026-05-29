# Coderr – Backend

> Kanban-based project management tool | REST API built with Django & Django
> REST Framework

Coderr is a platform for freelance developers where clients can post projects
and developers can offer their services. This repository contains **the backend only**,
which provides all data and business logic through a REST API. The corresponding
frontend communicates with this backend via these endpoints.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation & Configuration](#installation--configuration)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Author](#author)

---

## Prerequisites

- Python 3.14.5+
- pip 26.1.1+

---

## Installation & Configuration

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd Codere_Backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Mac/Linux
   .venv\Scripts\activate           # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file – sensitive settings are not stored directly in
   `core/settings.py` but loaded from a local `.env` file (ignored by Git):

   ```bash
   cp .env.template .env
   ```

5. Generate a new `SECRET_KEY` and add it to the `.env` file:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Add the generated key and the following values to your `.env` file:

   ```env
   SECRET_KEY='your_generated_key_here'
   DEBUG=True
   ```

   > **Note:** Use `DEBUG=True` for local development only. Set it to `False` in
   > production and update `ALLOWED_HOSTS` to match your actual domain.

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

   The API will be available at: `http://127.0.0.1:8000/`

---

## Project Structure

```
01_DEV/
├── core/               # Django project configuration (settings, urls, wsgi)
├── accounts/           # User management & authentication
│   └── api/            # Serializers, views, URLs for accounts
├── coderr/             # Core logic: boards, columns, tasks
│   └── api/            # Serializers, views, URLs for kan_mind
├── manage.py
└── requirements.txt
```

---

## API Endpoints

> For full endpoint documentation including request/response examples, status
> codes and permissions, see [docs/api.md](docs/api.md).

### Auth

| Method | Endpoint                      | Description                     | Auth required | Access         |
| ------ | ----------------------------- | ------------------------------- | ------------- | -------------- |
| POST   | `-`                           | -                               | No            | All            |




---

## Frontend

The corresponding frontend repository can be found here:

[Frontend Repository]()

---

## Author

**Philipp Biebert**  
Project status: 
