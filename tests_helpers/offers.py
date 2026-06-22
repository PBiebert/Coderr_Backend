from offers.models import Offer, OfferDetail


def offer_data(**kwargs):
    return {
        "title": "Graphic Design Package",
        "image": None,
        "description": "A comprehensive graphic design package for businesses.",
        "details": [
            {
                "title": "Basic Design",
                "revisions": 2,
                "delivery_time_in_days": 5,
                "price": 100,
                "features": ["Logo Design", "Business Card"],
                "offer_type": "basic",
            },
            {
                "title": "Standard Design",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 200,
                "features": ["Logo Design", "Business Card", "Letterhead"],
                "offer_type": "standard",
            },
            {
                "title": "Premium Design",
                "revisions": 10,
                "delivery_time_in_days": 10,
                "price": 500,
                "features": ["Logo Design", "Business Card", "Letterhead", "Flyer"],
                "offer_type": "premium",
            },
        ],
        **kwargs,
    }


def create_offer(business_user, offer_data):
    """Creates an offer with the given data and returns the created offer instance."""

    details = offer_data.pop("details")
    offer = Offer.objects.create(user=business_user, **offer_data)
    for detail in details:
        OfferDetail.objects.create(offer=offer, **detail)

    return offer
