from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import EmailLoginView, FarmerViewSet

router = DefaultRouter()
router.register(r'farmers', FarmerViewSet, basename='farmer')
# router.register(r'users', UserViewSet)
# router.register(r'farmers', FarmerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]