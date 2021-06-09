from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from django.views import View
from django.contrib.auth.views import LoginView

from django.http import HttpResponse

from registration.forms import AuthtificationForm, RegistrationForm, FormTableChange
from clubbisenes.models import UserProfileModel


class AuthtificationView(LoginView):
    template_name = 'registration/authtification.html'
    form_class = AuthtificationForm


class RegistrationView(View):
    def get(self, request):
        data = {
            'form': RegistrationForm
        }
        return render(request, 'registration/registration.html', data)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            new_user = form.save()
            UserProfileModel.objects.create(
                user=new_user,
                phone=phone
            )
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return render(request, "clubbisenes/index.html")

        else:
            return HttpResponse(form.errors)


class TableChange(View):
    def get(self, request):
        data = {


            'form': FormTableChange
        }
        return render(request, 'clubbisenes/changeTable.html', data)
