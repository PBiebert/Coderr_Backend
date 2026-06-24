from orders.models import Order


def order_data(customer_user, business_user, **kwargs):
    """
    Returns a dictionary with default order data, which can be overridden by
    providing additional keyword arguments.
    """

    return {
        "customer_user": customer_user,
        "business_user": business_user,
        "title": "Logo Design",
        "revisions": 3,
        "delivery_time_in_days": 5,
        "price": 150,
        "features": [
            "Logo Design",
            "Business Cards",
        ],
        "offer_type": "basic",
        "status": "in_progress",
        **kwargs,
    }


def create_order(order_data):
    """Creates an order with the given data and returns the created order instance."""

    return Order.objects.create(**order_data)
