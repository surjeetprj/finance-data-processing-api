from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # This is your actual "Login" endpoint
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # This endpoint gives a new access token when the old one expires
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]