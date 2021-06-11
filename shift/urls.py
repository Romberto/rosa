from django.urls import path
from . import views


urlpatterns = [
    path('open/', views.OpenShiftView.as_view(), name="openShift"),
    path('close/', views.CloseShiftView.as_view(), name="deleteShift")
]