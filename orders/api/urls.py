from django.urls import path, include
from .views import OrderListCreateAPIView, OrderDetailPatchDeleteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"orders", OrderDetailPatchDeleteViewSet, basename="orders")

urlpatterns = [
    path("orders/", OrderListCreateAPIView.as_view(), name="order-list"),
    path("", include(router.urls)),
]
