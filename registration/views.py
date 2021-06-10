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
            name = form.cleaned_data.get('username')
            passw = form.cleaned_data.get('password')
            user = User.objects.create_user(username=name, password=passw)
            user.save()
            phone = form.cleaned_data['phone']
            UserProfileModel.objects.create(
                user=user,
                phone=phone
            )
            name = form.cleaned_data.get('username')
            passw = form.cleaned_data.get('password')
            auth_user = authenticate(username=name, password=passw)
            if auth_user is not None:
                login(request, auth_user)

                return redirect('/reg/changeTable/')
            return HttpResponse('<h1>fuck</h1>')

        else:
            return HttpResponse('<h1>fuck222</h1>')


class TableChange(View):
    def get(self, request):
        data = {
            'form': FormTableChange
        }
        return render(request, 'clubbisenes/changeTable.html', data)

    def post(self, request):
        form = FormTableChange(request.POST)
        if form.is_valid():
            table = form.cleaned_data.get('numberTable')
            if request.user.is_authenticated:
                username = request.user.username
                user = User.objects.get(username=username)
                get_user = UserProfileModel.objects.get(user=user)
                get_user.table = table
                get_user.save()
                return redirect('/main/')

