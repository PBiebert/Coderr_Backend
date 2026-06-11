OFFER_DETAILS_BASIC = {
    "title": "Basic Design",
    "revisions": 2,
    "delivery_time_in_days": 5,
    "price": 100,
    "features": ["Logo Design", "Visitenkarte"],
    "offer_type": "basic",
}
OFFER_DETAILS_STANDARD = {
    "title": "Standard Design",
    "revisions": 5,
    "delivery_time_in_days": 7,
    "price": 200,
    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
    "offer_type": "standard",
}

OFFER_DETAILS_PREMIUM = {
    "title": "Premium Design",
    "revisions": 10,
    "delivery_time_in_days": 10,
    "price": 500,
    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
    "offer_type": "premium",
}

OFFER_DATA = {
    "title": "Grafikdesign-Paket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "details": [OFFER_DETAILS_BASIC, OFFER_DETAILS_STANDARD, OFFER_DETAILS_PREMIUM],
}


def offer_data():
    """Returns a dictionary with valid data for creating an offer."""

    return OFFER_DATA.copy()
