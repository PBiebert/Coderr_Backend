from django.urls import path
from .views import PlatformBaseInfoView

# from .views import

urlpatterns = [
    path("base-info/", PlatformBaseInfoView.as_view(), name="platform-base-info"),
]
