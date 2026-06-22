# Coderr – Backend

> Freelancer platform API | REST API built with Django & Django REST Framework

Coderr is a platform for freelance developers where customers can post requests
and business users can offer their services. This repository contains **the backend only**,
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
   cd Coderr_Backend
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
├── profiles/           # Profile management
│   └── api/            # Serializers, views, URLs for profiles
├── offers/             # Offer management
│   └── api/            # Serializers, views, URLs for offers
├── orders/             # Order management
│   └── api/            # Serializers, views, URLs for orders
├── order_statistics/   # Cross-cutting order statistics endpoints
│   └── api/            # Serializers, views, URLs for statistics
├── reviews/            # Review management
│   └── api/            # Serializers, views, URLs for reviews
├── manage.py
└── requirements.txt
```

---

## API Endpoints

> For full endpoint documentation including request/response examples, status
> codes and permissions, see [docs/api.md](docs/api.md).

### Authentication

| Method | Endpoint            | Description         | Auth required | Access |
| ------ | ------------------- | ------------------- | ------------- | ------ |
| POST   | `/api/registration/` | Register a new user | No            | All    |
| POST   | `/api/login/`        | Log in a user       | No            | All    |

### Profile

| Method | Endpoint                   | Description                        | Auth required | Access           |
| ------ | -------------------------- | ---------------------------------- | ------------- | ---------------- |
| GET    | `/api/profile/{pk}/`       | Retrieve one profile               | Yes           | Logged-in user   |
| PATCH  | `/api/profile/{pk}/`       | Update one profile                 | Yes           | Profile owner    |
| GET    | `/api/profiles/business/`  | List all business profiles         | Yes           | Logged-in user   |
| GET    | `/api/profiles/customer/`  | List all customer profiles         | Yes           | Logged-in user   |

### Offers

| Method | Endpoint                | Description                 | Auth required | Access                     |
| ------ | ----------------------- | --------------------------- | ------------- | -------------------------- |
| GET    | `/api/offers/`          | List all offers             | No            | All                        |
| POST   | `/api/offers/`          | Create a new offer          | Yes           | Business user              |
| GET    | `/api/offers/{id}/`     | Retrieve one offer          | Yes           | Logged-in user             |
| PATCH  | `/api/offers/{id}/`     | Update one offer            | Yes           | Offer owner                |
| DELETE | `/api/offers/{id}/`     | Delete one offer            | Yes           | Offer owner                |
| GET    | `/api/offerdetails/{id}/` | Retrieve one offer detail | Yes           | Logged-in user             |

### Orders

| Method | Endpoint                                | Description                                | Auth required | Access                  |
| ------ | --------------------------------------- | ------------------------------------------ | ------------- | ----------------------- |
| GET    | `/api/orders/`                          | List user-related orders                   | Yes           | Logged-in user          |
| POST   | `/api/orders/`                          | Create a new order                         | Yes           | Customer user           |
| PATCH  | `/api/orders/{id}/`                     | Update one order                           | Yes           | Business user           |
| DELETE | `/api/orders/{id}/`                     | Delete one order                           | Yes           | Business user           |
| GET    | `/api/order-count/{business_user_id}/`  | Count in-progress orders of a business user| Yes           | Logged-in user          |
| GET    | `/api/completed-order-count/{business_user_id}/` | Count completed orders of a business user | Yes      | Logged-in user          |

### Reviews

| Method | Endpoint              | Description            | Auth required | Access         |
| ------ | --------------------- | ---------------------- | ------------- | -------------- |
| GET    | `/api/reviews/`       | List all reviews       | Yes           | Logged-in user |
| POST   | `/api/reviews/`       | Create a review        | Yes           | Logged-in user |
| PATCH  | `/api/reviews/{id}/`  | Update a review        | Yes           | Review author  |
| DELETE | `/api/reviews/{id}/`  | Delete a review        | Yes           | Review author  |

### Cross-cutting Endpoints

| Method | Endpoint          | Description                                 | Auth required | Access |
| ------ | ----------------- | ------------------------------------------- | ------------- | ------ |
| GET    | `/api/base-info/` | Aggregated platform information for Coderr | No            | All    |

---

## Frontend

The corresponding frontend repository can be found here:

[Frontend Repository]()

---

## Author

**Philipp Biebert**  
Project status: 22.06.2026 (in progress)
