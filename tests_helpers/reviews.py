from reviews.models import Review


def review_data(customer_user, business_user, **kwargs):
    """Returns a dictionary with default review data, which can be overridden by providing additional keyword arguments."""

    return {
        "business_user": business_user,
        "reviewer": customer_user,
        "rating": 5,
        "description": "Great work! Highly recommended.",
        **kwargs,
    }


def create_review(review_data):
    """Creates an order with the given data and returns the created order instance."""

    return Review.objects.create(**review_data)
