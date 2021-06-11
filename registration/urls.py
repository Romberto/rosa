from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.AuthtificationView.as_view(), name="auth"),
    path('reg/', views.RegistrationView.as_view(), name="regist"),
    path('changeTable/', views.TableChange.as_view(), name="changeTable")
]