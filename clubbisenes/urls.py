from django.urls import path
from . import views

urlpatterns = [
    path('', views.club_list, name="clublist"),
    path('test/', views.Test.as_view(), name="test"),
    path('sound/', views.Sound.as_view(), name="sound"),
    path('logIn/', views.LogIn.as_view(), name="logIn"),
    path('cashier/', views.Cashier.as_view(), name="cashier"),
    path('dj/', views.Dj.as_view(), name="dj")
]
