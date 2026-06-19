from django.urls import path, include
from .views import (
    OrderListCreateAPIView,
    OrderDetailPatchDeleteViewSet,
    OrderCountAPIView,
    CompleteOrderCountAPIView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"orders", OrderDetailPatchDeleteViewSet, basename="orders")

urlpatterns = [
    path("orders/", OrderListCreateAPIView.as_view(), name="order-list"),
    path("order-count/<int:pk>/", OrderCountAPIView.as_view(), name="order-count"),
    path(
        "completed-order-count/<int:pk>/",
        CompleteOrderCountAPIView.as_view(),
        name="completed-order-count",
    ),
    path("", include(router.urls)),
]
