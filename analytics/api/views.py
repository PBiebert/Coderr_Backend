from rest_framework.generics import GenericAPIView
from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework.response import Response
from reviews.models import Review
from offers.models import Offer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

User = get_user_model()


class PlatformBaseInfoView(GenericAPIView):
    """API view to retrieve platform base information."""

    permission_classes = [AllowAny]

    def get(self, request):
        """Handle GET request to retrieve platform base information."""

        review_count = Review.objects.all().count()
        average_rating = Review.objects.aggregate(average=Round(Avg("rating"), 1)).get(
            "average", 0.0
        )
        business_profile_count = User.objects.filter(type="business").count()
        offer_count = Offer.objects.all().count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }

        return Response(data)
