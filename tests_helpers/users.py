from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from profiles.models import Profile
from rest_framework.test import APIClient

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
    """Creates and returns a customer user with a profile."""

    data = CUSTOMER_USER_DATA.copy()
    data.pop("repeated_password")
    user = User.objects.create_user(**data)
    Profile.objects.create(user=user)
    return user


def create_business_user():
    """Creates and returns a business user with a profile."""

    data = BUSINESS_USER_DATA.copy()
    data.pop("repeated_password")
    user = User.objects.create_user(**data)
    Profile.objects.create(user=user)
    return user


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
