from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from django.http import HttpResponse

from clubbisenes.views import shiftDecoration
from registration.forms import AuthtificationForm, RegistrationForm, FormTableChange
from clubbisenes.models import UserProfileModel


class AuthtificationView(View):

    def get(self, requests, *args, **kwargs):
        form = AuthtificationForm(requests.POST or None)
        data = {
            'form': form,
            'error': form.errors
        }
        return render(requests, 'registration/authtification.html', data)

    def post(self, requests):
        form = AuthtificationForm(requests.POST or None)
        if form.is_valid():
            userName = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=userName, password=password)
            if user:
                login(requests, user)
                try:
                    table = requests.user.profile.table
                    if table:
                        return redirect('/')
                except AttributeError:
                    return redirect('/')
                return HttpResponseRedirect('/reg/changeTable')

        return render(requests, 'registration/authtification.html', {'form': form, 'error': form.errors})


class RegistrationView(View):
    @shiftDecoration
    def get(self, request):
        form = RegistrationForm()
        data = {
            'form': form,
            'error': form.errors
        }
        return render(request, 'registration/registration.html', data)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            passw = form.cleaned_data.get('password')
            user = User.objects.create_user(username=name, password=passw)
            phone = form.cleaned_data['phone']

            UserProfileModel.objects.create(
                user=user,
                phone=phone
            )

            group = Group.objects.get(name='clients')
            group.user_set.add(user)
            name = form.cleaned_data.get('username')
            passw = form.cleaned_data.get('password')
            auth_user = authenticate(username=name, password=passw)
            if auth_user is not None:
                login(request, auth_user)

                return redirect('/reg/changeTable/')
            return HttpResponse('<h1>ошибка авторизации</h1>')

        else:
            data = {
                'form': form,
                'error': form.errors
            }
            return render(request, 'registration/registration.html', data)


class TableChange(View):
    @shiftDecoration
    def get(self, request):
        data = {
            'form': FormTableChange
        }
        return render(request, 'clubbisenes/changeTable.html', data)

    def post(self, request):
        form = FormTableChange(request.POST)
        if form.is_valid():
            table = form.cleaned_data.get('numberTable')
            try:
                user = UserProfileModel.objects.get(user=request.user)
                if user:
                    user.table = table
                    user.save()
            except ValueError:
                UserProfileModel.objects.create(
                    user=request.user,
                    table=table
                )
            return redirect('/')
        else:
            return HttpResponse('<h1>ошибка валидации формы CT</h1>')
