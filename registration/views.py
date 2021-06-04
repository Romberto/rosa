from django.shortcuts import render, redirect

from django.views import View 
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from registration.forms import AuthtificationForm, RegistrationForm




class AuthtificationView(LoginView):
    template_name = 'registration/authtification.html'
    form_class = AuthtificationForm

class RegistrationView(View):
    def get(self, request):
        data = {
            'form': RegistrationForm
        }
        return render(request, 'registration/registration.html', data)