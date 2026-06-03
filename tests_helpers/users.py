from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

CUSTOMER_USER_DATA = {
    "username": "exampleCustomerUsername",
    "email": "exampleCustomer@mail.de",
    "password": "examplePassword",
    "repeated_password": "examplePassword",
    "type": "customer",
}

BUSINESS_USER_DATA = {
    "username": "exampleBusinessUsername",
    "email": "exampleBusinessUsername@mail.de",
    "password": "examplePassword",
    "repeated_password": "examplePassword",
    "type": "business",
}


def customer_registration_data():
    """Returns a dictionary with valid registration data for a customer user."""
    return CUSTOMER_USER_DATA.copy()


def business_registration_data():
    """Returns a dictionary with valid registration data for a business user."""
    return BUSINESS_USER_DATA.copy()


def create_customer_user():
    """Creates a customer user and returns the user and token."""

    data = CUSTOMER_USER_DATA.copy()
    data.pop("repeated_password")
    user = User.objects.create_user(**data)
    token, created = Token.objects.get_or_create(user=user)
    return user, token


def create_business_user():
    """Creates a business user and returns the user and token."""

    data = BUSINESS_USER_DATA.copy()
    data.pop("repeated_password")
    user = User.objects.create_user(**data)
    token, created = Token.objects.get_or_create(user=user)
    return user, token


def customer_login_data():
    """Returns a dictionary with valid login data for a customer user."""

    data = {
        "username": CUSTOMER_USER_DATA["username"],
        "password": CUSTOMER_USER_DATA["password"],
    }
    return data


def business_login_data():
    """Returns a dictionary with valid login data for a business user."""

    data = {
        "username": BUSINESS_USER_DATA["username"],
        "password": BUSINESS_USER_DATA["password"],
    }
    return data
