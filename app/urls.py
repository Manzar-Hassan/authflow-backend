from django.contrib import admin
from django.urls import path
from users.views import RegisterView, LoginView, DashboardView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/signup/', RegisterView.as_view(), name="auth_register"),
    path('api/auth/signin/', LoginView.as_view(), name="auth_signin"),
    # path('api/auth/logout/', LogoutView.as_view(), name="auth_logout"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard')
]
