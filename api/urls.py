from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import RegisterView

urlpatterns = [
    #Register
    path('register/',RegisterView.as_view(),name="register"),
]