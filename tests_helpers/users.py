from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from profiles.models import Profile
from rest_framework.test import APIClient

User = get_user_model()

USER_DATA = {
    "username": "exampleUsername",
    "email": "example@mail.de",
    "password": "examplePassword",
    "repeated_password": "examplePassword",
    "type": "customer",
}


def user_registration_data():
    """Returns a dictionary with valid registration data for a user."""

    return USER_DATA.copy()


def create_user(**kwargs):
    """Creates and returns a user with a profile."""

    data = USER_DATA.copy()
    data.update(kwargs)
    data.pop("repeated_password")
    user = User.objects.create_user(**data)
    Profile.objects.create(user=user)
    return user


def user_login_data():
    """Returns a dictionary with valid login data for user."""

    data = {
        "username": USER_DATA["username"],
        "password": USER_DATA["password"],
    }
    return data


def fill_database_with_users():
    """Fills the database with multiple users for testing purposes."""

    for i in range(1, 2):
        create_user(
            username=f"exampleCustomUsername{i}",
            email=f"exampleCustom{i}@mail.de",
            type="customer",
        )

        create_user(
            username=f"exampleBusinessUsername{i}",
            email=f"examplebusiness{i}@mail.de",
            type="business",
        )
