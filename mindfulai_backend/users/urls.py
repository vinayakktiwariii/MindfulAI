# from django.urls import path
# from . import views

# urlpatterns = [
#     path('register/', views.RegisterView.as_view(), name='register'),
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('logout/', views.LogoutView.as_view(), name='logout'),
#     path('profile/', views.ProfileView.as_view(), name='profile'),
#     path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
#     path('password/reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
#     path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
# ]

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.get_current_user, name='current_user'),
]
