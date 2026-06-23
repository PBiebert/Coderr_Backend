from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()


def user_registration_data():
    """Returns a dictionary with valid registration data for a user."""

    return {
        "username": "exampleUsername",
        "email": "example@mail.de",
        "password": "examplePassword",
        "repeated_password": "examplePassword",
        "type": "customer",
    }


def create_user(**kwargs):
    """Creates and returns a user with a profile."""

    data = user_registration_data()
    data.update(kwargs)
    data.pop("repeated_password")
    user = User.objects.create_user(**data)
    Profile.objects.create(user=user)
    return user


def user_login_data():
    """Returns a dictionary with valid login data for user."""

    data = {
        "username": "exampleUsername",
        "password": "examplePassword",
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
