PROFILE_UPDATE_DATA = {
    "first_name": "Max",
    "last_name": "Mustermann",
    "location": "Berlin",
    "tel": "987654321",
    "description": "Updated business description",
    "working_hours": "10-18",
    "email": "new_email@business.de",
}


def profile_update_data():
    """Returns a dictionary with valid data for updating a profile."""

    return PROFILE_UPDATE_DATA.copy()
