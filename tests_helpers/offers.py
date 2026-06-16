from .users import create_user
from offers.models import Offer, OfferDetail

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


def offer_data(**kwargs):
    """Returns a dictionary with default offer data, which can be overridden by passing keyword arguments."""

    data = OFFER_DATA.copy()
    data.update(kwargs)
    return data


def create_offer(business_user, offer_data):
    """Creates an offer with the given data and returns the created offer instance."""

    details = offer_data.pop("details")
    offer = Offer.objects.create(user=business_user, **offer_data)
    for detail in details:
        OfferDetail.objects.create(offer=offer, **detail)

    return offer
