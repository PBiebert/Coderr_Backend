# Coderr – API-Dokumentation

Basis-URL: http://127.0.0.1:8000/api/  
Authentifizierung: Token-basiert (`Authorization: Token <dein_token>`)

---

## Inhaltsverzeichnis

- Authentifizierung
  - [POST /registration/](#post-registration)
  - POST /login/

---

## Authentication

### POST /registration/

Registriert ein neues Benutzerkonto.

**Auth required:** No

**Request Body**

```json
{
  "username": "exampleUsername",
  "email": "example@mail.de",
  "password": "examplePassword",
  "repeated_password": "examplePassword",
  "type": "customer"
}
```

**Success Response `201`**

```json
{
  "token": "83bf098723b08f7b23429u0fv8274",
  "username": "exampleUsername",
  "email": "example@mail.de",
  "user_id": 1
}
```

**Status Codes**

| Code | Beschreibung                                                       |
| ---- | ------------------------------------------------------------------ |
| 201  | User successfully registered.                                      |
| 400  | Invalid data                                                       |

---