# Coderr - API Documentation

Base URL: `http://127.0.0.1:8000/api/`  
Authentication: Token-based (`Authorization: Token <your_token>`)

---

## Table of Contents

- [Authentication](#authentication)
  - [POST /registration/](#post-registration)
  - [POST /login/](#post-login)
- [Profile](#profile)
  - [GET /profile/{pk}/](#get-profilepk)
  - [PATCH /profile/{pk}/](#patch-profilepk)
  - [GET /profiles/business/](#get-profilesbusiness)
  - [GET /profiles/customer/](#get-profilescustomer)
- [Offers](#offers)
  - [GET /offers/](#get-offers)
  - [POST /offers/](#post-offers)
  - [GET /offers/{id}/](#get-offersid)
  - [PATCH /offers/{id}/](#patch-offersid)
  - [DELETE /offers/{id}/](#delete-offersid)
  - [GET /offerdetails/{id}/](#get-offerdetailsid)
- [Orders](#orders)
  - [GET /orders/](#get-orders)
  - [POST /orders/](#post-orders)
  - [PATCH /orders/{id}/](#patch-ordersid)
  - [DELETE /orders/{id}/](#delete-ordersid)
  - [GET /order-count/{business_user_id}/](#get-order-countbusiness_user_id)
  - [GET /completed-order-count/{business_user_id}/](#get-completed-order-countbusiness_user_id)
- [Reviews](#reviews)
  - [GET /reviews/](#get-reviews)
  - [POST /reviews/](#post-reviews)
  - [PATCH /reviews/{id}/](#patch-reviewsid)
  - [DELETE /reviews/{id}/](#delete-reviewsid)
- [Cross-cutting Endpoints](#cross-cutting-endpoints)
  - [GET /base-info/](#get-base-info)

---

## Authentication

### POST /registration/

Creates a new user. The user type can be either `customer` or `business`.

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
  "user_id": 123
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 201  | User was created successfully. |
| 400  | Invalid request data. |
| 500  | Internal server error. |

**Rate Limits:** No limit  
**Permissions:** No permissions required

---

### POST /login/

Authenticates a user and returns an auth token for subsequent API requests.

**Auth required:** No

**Request Body**

```json
{
  "username": "exampleUsername",
  "password": "examplePassword"
}
```

**Success Response `200`**

```json
{
  "token": "83bf098723b08f7b23429u0fv8274",
  "username": "exampleUsername",
  "email": "example@mail.de",
  "user_id": 123
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Login successful. |
| 400  | Invalid request data. |
| 500  | Internal server error. |

**Rate Limits:** No limit  
**Permissions:** No permissions required

---

## Profile

### GET /profile/{pk}/

Returns detailed profile information for a specific user (`customer` or `business`).

**Auth required:** Yes  
**Permissions:** Authenticated user

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| pk | integer | ID of the user whose profile is requested. |

**Success Response `200`**

```json
{
  "user": 1,
  "username": "max_mustermann",
  "first_name": "Max",
  "last_name": "Mustermann",
  "file": "profile_picture.jpg",
  "location": "Berlin",
  "tel": "123456789",
  "description": "Business description",
  "working_hours": "9-17",
  "type": "business",
  "email": "max@business.de",
  "created_at": "2023-01-01T12:00:00Z"
}
```

The fields `first_name`, `last_name`, `location`, `tel`, `description`, and `working_hours`
must not be `null` in responses. Use empty strings (`""`) if no values are available.

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Profile data returned successfully. |
| 401  | User is not authenticated. |
| 404  | Profile was not found. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

### PATCH /profile/{pk}/

Updates selected profile information.

**Auth required:** Yes  
**Permissions:** Only the profile owner can update the profile

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| pk | integer | ID of the user profile to update. |

**Request Body**

```json
{
  "first_name": "Max",
  "last_name": "Mustermann",
  "location": "Berlin",
  "tel": "987654321",
  "description": "Updated business description",
  "working_hours": "10-18",
  "email": "new_email@business.de"
}
```

**Success Response `200`**

```json
{
  "user": 1,
  "username": "max_mustermann",
  "first_name": "Max",
  "last_name": "Mustermann",
  "file": "profile_picture.jpg",
  "location": "Berlin",
  "tel": "987654321",
  "description": "Updated business description",
  "working_hours": "10-18",
  "type": "business",
  "email": "new_email@business.de",
  "created_at": "2023-01-01T12:00:00Z"
}
```

The fields `first_name`, `last_name`, `location`, `tel`, `description`, and `working_hours`
must not be `null` in responses. Use empty strings (`""`) if no values are available.

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Profile updated successfully. |
| 401  | User is not authenticated. |
| 403  | Authenticated user is not the profile owner. |
| 404  | Profile was not found. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

### GET /profiles/business/

Returns a list of all business profiles on the platform.

**Auth required:** Yes  
**Permissions:** Authenticated user

**Success Response `200`**

```json
[
  {
    "user": 1,
    "username": "max_business",
    "first_name": "Max",
    "last_name": "Mustermann",
    "file": "profile_picture.jpg",
    "location": "Berlin",
    "tel": "123456789",
    "description": "Business description",
    "working_hours": "9-17",
    "type": "business"
  }
]
```

The fields `first_name`, `last_name`, `location`, `tel`, `description`, and `working_hours`
must not be `null` in responses. Use empty strings (`""`) if no values are available.

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Business profile list returned successfully. |
| 401  | User is not authenticated. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

### GET /profiles/customer/

Returns a list of all customer profiles on the platform.

**Auth required:** Yes  
**Permissions:** Authenticated user

**Success Response `200`**

```json
[
  {
    "user": 2,
    "username": "customer_jane",
    "first_name": "Jane",
    "last_name": "Doe",
    "file": "profile_picture_customer.jpg",
    "uploaded_at": "2023-09-15T09:00:00",
    "type": "customer"
  }
]
```

The fields `first_name`, `last_name`, `location`, `tel`, `description`, and `working_hours`
must not be `null` in responses. Use empty strings (`""`) if no values are available.

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Customer profile list returned successfully. |
| 401  | User is not authenticated. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

## Offers

### GET /offers/

Returns a list of offers including offer detail links, minimum price, and shortest delivery time.

**Auth required:** No

**Query Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| creator_id | integer | Filter offers by creator ID. |
| min_price | float | Filter offers by minimum price. |
| max_delivery_time | integer | Filter offers whose delivery time is less than or equal to this value. |
| ordering | string | Sort by `updated_at` or `min_price`. |
| search | string | Search in `title` and `description`. |
| page_size | integer | Number of results per page. |

**Success Response `200`**

```json
{
  "count": 1,
  "next": "http://127.0.0.1:8000/api/offers/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "title": "Website Design",
      "image": null,
      "description": "Professional website design...",
      "created_at": "2024-09-25T10:00:00Z",
      "updated_at": "2024-09-28T12:00:00Z",
      "details": [
        {
          "id": 1,
          "url": "/offerdetails/1/"
        },
        {
          "id": 2,
          "url": "/offerdetails/2/"
        },
        {
          "id": 3,
          "url": "/offerdetails/3/"
        }
      ],
      "min_price": 100,
      "min_delivery_time": 7,
      "user_details": {
        "first_name": "John",
        "last_name": "Doe",
        "username": "jdoe"
      }
    }
  ]
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Request successful and offer list returned. |
| 400  | Invalid query parameters. |
| 500  | Internal server error. |

**Rate Limits:** No limit  
**Permissions:** No permissions required  
**Extra Information:** Response uses page number pagination.

---

### POST /offers/

Creates a new offer. An offer must contain exactly 3 details.

**Auth required:** Yes  
**Permissions:** Authenticated user with profile type `business`

**Request Body**

```json
{
  "title": "Graphic Design Package",
  "image": null,
  "description": "A complete graphic design package for businesses.",
  "details": [
    {
      "title": "Basic Design",
      "revisions": 2,
      "delivery_time_in_days": 5,
      "price": 100,
      "features": [
        "Logo Design",
        "Business Card"
      ],
      "offer_type": "basic"
    },
    {
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 7,
      "price": 200,
      "features": [
        "Logo Design",
        "Business Card",
        "Letterhead"
      ],
      "offer_type": "standard"
    },
    {
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 500,
      "features": [
        "Logo Design",
        "Business Card",
        "Letterhead",
        "Flyer"
      ],
      "offer_type": "premium"
    }
  ]
}
```

**Success Response `201`**

```json
{
  "id": 1,
  "title": "Graphic Design Package",
  "image": null,
  "description": "A complete graphic design package for businesses.",
  "details": [
    {
      "id": 1,
      "title": "Basic Design",
      "revisions": 2,
      "delivery_time_in_days": 5,
      "price": 100,
      "features": [
        "Logo Design",
        "Business Card"
      ],
      "offer_type": "basic"
    },
    {
      "id": 2,
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 7,
      "price": 200,
      "features": [
        "Logo Design",
        "Business Card",
        "Letterhead"
      ],
      "offer_type": "standard"
    },
    {
      "id": 3,
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 500,
      "features": [
        "Logo Design",
        "Business Card",
        "Letterhead",
        "Flyer"
      ],
      "offer_type": "premium"
    }
  ]
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 201  | Offer created successfully. |
| 400  | Invalid request data or incomplete details. |
| 401  | User is not authenticated. |
| 403  | Authenticated user is not of type `business`. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

### GET /offers/{id}/

Returns details for one specific offer by ID.

**Auth required:** Yes  
**Permissions:** Authenticated user

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | integer | ID of the requested offer. |

**Success Response `200`**

```json
{
  "id": 66,
  "user": 114,
  "title": "Graphic Design Package",
  "image": null,
  "description": "A complete graphic design package for businesses.",
  "created_at": "2025-01-23T07:44:15.365773Z",
  "updated_at": "2025-01-23T07:44:15.365773Z",
  "details": [
    {
      "id": 199,
      "url": "http://127.0.0.1:8000/api/offerdetails/199/"
    },
    {
      "id": 200,
      "url": "http://127.0.0.1:8000/api/offerdetails/200/"
    },
    {
      "id": 201,
      "url": "http://127.0.0.1:8000/api/offerdetails/201/"
    }
  ],
  "min_price": 50,
  "min_delivery_time": 5
}
```

`user` is the ID of the user who created the offer.

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Offer returned successfully. |
| 401  | User is not authenticated. |
| 404  | Offer not found. |
| 500  | Internal server error. |

**Rate Limits:** No limit  
**Extra Information:** Offer details include URLs to detail resources.

---

### PATCH /offers/{id}/

Partially updates a specific offer. Only provided fields are updated.

**Auth required:** Yes  
**Permissions:** Offer owner

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | integer | ID of the offer to update. |

**Request Body**

```json
{
  "title": "Updated Graphic Design Package",
  "details": [
    {
      "title": "Basic Design Updated",
      "revisions": 3,
      "delivery_time_in_days": 6,
      "price": 120,
      "features": [
        "Logo Design",
        "Flyer"
      ],
      "offer_type": "basic"
    }
  ]
}
```

**Success Response `200`**

```json
{
  "id": 66,
  "title": "Updated Graphic Design Package",
  "image": null,
  "description": "A complete graphic design package for businesses.",
  "details": [
    {
      "id": 199,
      "title": "Basic Design Updated",
      "revisions": 3,
      "delivery_time_in_days": 6,
      "price": 120,
      "features": [
        "Logo Design",
        "Flyer"
      ],
      "offer_type": "basic"
    },
    {
      "id": 200,
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 10,
      "price": 120,
      "features": [
        "Logo Design",
        "Business Card",
        "Letterhead"
      ],
      "offer_type": "standard"
    },
    {
      "id": 201,
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 150,
      "features": [
        "Logo Design",
        "Business Card",
        "Letterhead",
        "Flyer"
      ],
      "offer_type": "premium"
    }
  ]
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Offer updated successfully. |
| 400  | Invalid request data or incomplete details. |
| 401  | User is not authenticated. |
| 403  | Authenticated user is not the owner of the offer. |
| 404  | Offer not found. |
| 500  | Internal server error. |

**Rate Limits:** No limit  
**Extra Information:**
- Only provided fields are updated.
- Non-provided fields remain unchanged.
- Offer details can be updated individually; detail IDs remain unchanged.
- Include `offer_type` to uniquely identify each detail payload.

---

### DELETE /offers/{id}/

Deletes a specific offer by ID.

**Auth required:** Yes  
**Permissions:** Offer owner

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | integer | ID of the offer to delete. |

**Success Response `204`** - No content

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 204  | Offer deleted successfully. |
| 401  | User is not authenticated. |
| 403  | Authenticated user is not the owner of the offer. |
| 404  | Offer not found. |
| 500  | Internal server error. |

**Rate Limits:** No limit  
**Extra Information:** The endpoint returns no response body on success.

---

### GET /offerdetails/{id}/

Returns details of one specific offer detail resource.

**Auth required:** Yes  
**Permissions:** Authenticated user

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | integer | ID of the offer detail resource. |

**Success Response `200`**

```json
{
  "id": 1,
  "title": "Basic Design",
  "revisions": 2,
  "delivery_time_in_days": 5,
  "price": 100,
  "features": [
    "Logo Design",
    "Business Card"
  ],
  "offer_type": "basic"
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Offer detail returned successfully. |
| 401  | User is not authenticated. |
| 404  | Offer detail not found. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

## Orders

### GET /orders/

Returns a list of orders linked to the authenticated user, either as customer or business user.

**Auth required:** Yes  
**Permissions:** Authenticated user

**Success Response `200`**

```json
[
  {
    "id": 1,
    "customer_user": 1,
    "business_user": 2,
    "title": "Logo Design",
    "revisions": 3,
    "delivery_time_in_days": 5,
    "price": 150,
    "features": [
      "Logo Design",
      "Business Cards"
    ],
    "offer_type": "basic",
    "status": "in_progress",
    "created_at": "2024-09-29T10:00:00Z",
    "updated_at": "2024-09-30T12:00:00Z"
  }
]
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Orders returned successfully. |
| 401  | User is not authenticated. |
| 500  | Internal server error. |

**Rate Limits:** No limit  
**Extra Information:** Only orders associated with the authenticated user are returned.

---

### POST /orders/

Creates a new order based on an offer detail.

**Auth required:** Yes  
**Permissions:** Authenticated user with profile type `customer`

**Request Body**

```json
{
  "offer_detail_id": 1
}
```

**Success Response `201`**

```json
{
  "id": 1,
  "customer_user": 1,
  "business_user": 2,
  "title": "Logo Design",
  "revisions": 3,
  "delivery_time_in_days": 5,
  "price": 150,
  "features": [
    "Logo Design",
    "Business Cards"
  ],
  "offer_type": "basic",
  "status": "in_progress",
  "created_at": "2024-09-29T10:00:00Z",
  "updated_at": "2024-09-30T12:00:00Z"
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 201  | Order created successfully. |
| 400  | Invalid request data (for example missing or invalid `offer_detail_id`). |
| 401  | User is not authenticated. |
| 403  | User has no permission (for example not type `customer`). |
| 404  | Referenced offer detail not found. |
| 500  | Internal server error. |

**Rate Limits:** No limit  
**Extra Information:** Only users of type `customer` can create orders.

---

### PATCH /orders/{id}/

Updates the status of a specific order. Typical status values: `in_progress`, `completed`, `cancelled`.

**Auth required:** Yes  
**Permissions:** Authenticated user with profile type `business`

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | integer | ID of the order to update. |

**Request Body**

```json
{
  "status": "completed"
}
```

**Success Response `200`**

```json
{
  "id": 1,
  "customer_user": 1,
  "business_user": 2,
  "title": "Logo Design",
  "revisions": 3,
  "delivery_time_in_days": 5,
  "price": 150,
  "features": [
    "Logo Design",
    "Business Cards"
  ],
  "offer_type": "basic",
  "status": "completed",
  "created_at": "2024-09-29T10:00:00Z",
  "updated_at": "2024-09-30T15:00:00Z"
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Order status updated successfully. |
| 400  | Invalid status value or invalid payload. |
| 401  | User is not authenticated. |
| 403  | User has no permission to update this order. |
| 404  | Order not found. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

### DELETE /orders/{id}/

Deletes a specific order. This action is restricted to admin/staff users.

**Auth required:** Yes  
**Permissions:** Admin/staff only

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | integer | ID of the order to delete. |

**Success Response `204`** - No content

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 204  | Order deleted successfully. |
| 401  | User is not authenticated. |
| 403  | User has no permission to delete this order. |
| 404  | Order not found. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

### GET /order-count/{business_user_id}/

Returns the number of in-progress orders for a specific business user.

**Auth required:** Yes  
**Permissions:** Authenticated user

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| business_user_id | integer | ID of the business user. |

**Success Response `200`**

```json
{
  "order_count": 5
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | In-progress order count returned successfully. |
| 401  | User is not authenticated. |
| 404  | No business user found for the given ID. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

### GET /completed-order-count/{business_user_id}/

Returns the number of completed orders for a specific business user.

**Auth required:** Yes  
**Permissions:** Authenticated user

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| business_user_id | integer | ID of the business user. |

**Success Response `200`**

```json
{
  "completed_order_count": 10
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Completed order count returned successfully. |
| 401  | User is not authenticated. |
| 404  | No business user found for the given ID. |
| 500  | Internal server error. |

**Rate Limits:** No limit

---

## Reviews

### GET /reviews/

Returns all reviews. Reviews can be filtered and ordered.

**Auth required:** Yes  
**Permissions:** Any authenticated user

**Query Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| business_user_id | integer | Filter by business user ID. |
| reviewer_id | integer | Filter by reviewer ID. |
| ordering | string | Order by `updated_at` or `rating`. |

**Success Response `200`**

```json
[
  {
    "id": 1,
    "business_user": 2,
    "reviewer": 3,
    "rating": 4,
    "description": "Very professional service.",
    "created_at": "2023-10-30T10:00:00Z",
    "updated_at": "2023-10-31T10:00:00Z"
  },
  {
    "id": 2,
    "business_user": 5,
    "reviewer": 3,
    "rating": 5,
    "description": "Top quality and fast delivery.",
    "created_at": "2023-09-20T10:00:00Z",
    "updated_at": "2023-09-20T12:00:00Z"
  }
]
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Review list returned successfully. |
| 401  | Unauthorized. User must be authenticated. |
| 500  | Internal server error. |

---

### POST /reviews/

Creates a new review for a business user. Only authenticated users with a customer profile may create reviews. One user can leave only one review per business profile.

**Auth required:** Yes  
**Permissions:** Authenticated user with profile type `customer`

**Request Body**

```json
{
  "business_user": 2,
  "rating": 4,
  "description": "Everything was great!"
}
```

**Success Response `201`**

```json
{
  "id": 3,
  "business_user": 2,
  "reviewer": 3,
  "rating": 4,
  "description": "Everything was great!",
  "created_at": "2023-10-30T15:30:00Z",
  "updated_at": "2023-10-30T15:30:00Z"
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 201  | Review created successfully. |
| 400  | Bad request (for example duplicate review for same business profile). |
| 401  | Unauthorized. User must be authenticated and have a customer profile. |
| 403  | Forbidden. User can only create one review per business profile. |
| 500  | Internal server error. |

**Extra Information:** Customers can submit one review per business user.

---

### PATCH /reviews/{id}/

Updates selected fields of an existing review. Only `rating` and `description` are editable. Only the review creator may update it.

**Auth required:** Yes  
**Permissions:** Review creator only

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | integer | ID of the review to update. |

**Request Body**

```json
{
  "rating": 5,
  "description": "Even better than expected!"
}
```

**Success Response `200`**

```json
{
  "id": 1,
  "business_user": 2,
  "reviewer": 3,
  "rating": 5,
  "description": "Even better than expected!",
  "created_at": "2023-10-30T10:00:00Z",
  "updated_at": "2023-11-01T08:00:00Z"
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Review updated successfully. |
| 400  | Bad request. Invalid payload. |
| 401  | Unauthorized. User must be authenticated. |
| 403  | Forbidden. User has no permission to update this review. |
| 404  | Review not found. |

---

### DELETE /reviews/{id}/

Deletes a specific review. Only the review creator may delete it.

**Auth required:** Yes  
**Permissions:** Review creator only

**URL Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | integer | ID of the review to delete. |

**Success Response `204`** - No content

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 204  | Review deleted successfully. |
| 401  | Unauthorized. User must be authenticated. |
| 403  | Forbidden. User has no permission to delete this review. |
| 404  | Review not found. |

---

## Cross-cutting Endpoints

### GET /base-info/

Returns aggregated platform statistics, including review totals, average rating,
business profile count, and offer count.

**Auth required:** No

**Success Response `200`**

```json
{
  "review_count": 10,
  "average_rating": 4.6,
  "business_profile_count": 45,
  "offer_count": 150
}
```

**Status Codes**

| Code | Description |
| ---- | ----------- |
| 200  | Base info returned successfully. |
| 500  | Internal server error. |

**Rate Limits:** No limit  
**Permissions:** No permissions required  
**Extra Information:** `average_rating` is rounded to one decimal place.
