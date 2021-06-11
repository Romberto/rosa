from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [

    path('main/', views.Main.as_view(), name="main"),
    path('test/', views.Test.as_view(), name="test"),
    path('sound/', views.Sound.as_view(), name="sound"),
    path('logIn/', views.LogIn.as_view(), name="logIn"),
    path('cashier/', views.Cashier.as_view(), name="cashier"),
    path('dj/', views.Dj.as_view(), name="dj"),
    path('dj/<int:pk>', views.SoundModerationView.as_view(), name="djView"),
    path('dj/play/<int:pk>', views.DjPlay.as_view(), name="djPlay"),
    path('auth/', views.Authenticate.as_view(), name="authenticate"),
    path('creat', views.bdFull.as_view(), name="create")

]
