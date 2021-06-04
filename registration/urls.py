from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('login/', views.AuthtificationView.as_view(), name="auth"),
    path('reg', views.RegistrationView.as_view(), name="regist")]