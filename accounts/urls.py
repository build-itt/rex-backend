from django.urls import path,include
from .views import *
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

urlpatterns = [
    path('history/', DashboardView.as_view(), name="history"),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password/reset/', reset_password_request_token, name='password_reset'),
    path('passwordreset/confirm/', reset_password_confirm, name='password_reset_confirm'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
]