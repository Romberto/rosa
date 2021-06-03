from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView
from .models import Sounds, SoundStatus, UserProfileModel, Table, ShiftUser
from .forms import SoundForms, ModerationForm, PlayForm, PayForm, AuthForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from random import randint


def shiftDecoration(func):
    def wraper(self, request):
        shistState = ShiftUser.objects.filter(state=True)
        if not shistState:
            data = {
                'AuthForm': AuthForm(),

            }

            return render(request, 'clubbisenes/logIn.html', data)
        return func(self, request)

    return wraper

    return wraper


class Authenticate(View):
    @shiftDecoration
    def get(self, request):
        table = int(request.GET['table'])
        user_day = User.objects.get(username='table-10_user-1')
        password = user_day.password
        table_db = Table.objects.get(number=table)
        users = UserProfileModel.objects.filter(table=table_db)
        for _user in users:
            if _user.activate == False:
                user_name = _user.user.username
                user = authenticate(username=user_name, password='12345')
                if user.is_active:
                    login(request, user)

                    data = {'user': user_name,
                            'table': table,
                            'users': password,
                            'sounds': Sounds.objects.filter(status=4).order_by('-id')[:3:-1],
                            'wait_mod': Sounds.objects.filter(status=2).order_by('-id')[:3:-1]
                            }
                    return render(request, 'clubbisenes/index.html', data)


class Main(View):
    def get(self, request):
        table = request.user.profile.table
        data = {
            'table': table,
            'sounds': Sounds.objects.filter(status=4).order_by('-id')[:3:-1],
            'wait_mod': Sounds.objects.filter(status=2).order_by('-id')[:3:-1]
        }

        return render(request, 'clubbisenes/index.html', data)


class Test(View):
    def get(self, request):
        return render(request, 'clubbisenes/test.html', {})


class Sound(View):
    @shiftDecoration
    def get(self, request):
        sound_form = SoundForms()
        number = request.user.profile.table
        return render(request, 'clubbisenes/sound.html', {'sound_form': sound_form, 'number': number})

    def post(self, request):
        form = SoundForms(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            new_sound = Sounds(**data)
            new_sound.user = request.user
            new_sound.table = request.user.profile.table
            new_sound.save()
            return redirect('/auth?table=' + str(new_sound.table.number))
        else:
            return redirect('/auth')


class LogIn(View):
    @shiftDecoration
    def get(self, request):
        data = {
            'AuthForm': AuthForm(),

        }

        return render(request, 'clubbisenes/logIn.html', data)

    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user = authenticate(username=name, password=password)
            if user and user.is_active and role == 'K':
                if user.groups.filter(name="cachers").exists():
                    login(request, user)
                    return redirect('/cashier')
                else:
                    return render(request, 'clubbisenes/test.html')
            elif user and user.is_active and role == 'D':
                if user.groups.filter(name="djs").exists():
                    login(request, user)
                    return redirect('/dj')
                else:
                    return render(request, 'clubbisenes/test.html')
            else:
                return redirect('/test')


class Cashier(View):
    def get(self, request):
        if request.user.groups.filter(name="cachers").exists():
            data = {'wait_pay': Sounds.objects.filter(status=3),
                    'payForm': PayForm(),
                    'state': ShiftUser.objects.filter(state=True),
                    'post_sounds_count': Sounds.objects.filter(status=4).count()}
            return render(request, 'clubbisenes/cashier.html', data)
        else:
            return redirect('/test')

    def post(self, requests):
        form = PayForm(requests.POST)
        if form.is_valid():
            soundId = form.cleaned_data.get('pay')
            sound = Sounds.objects.get(id=int(soundId))
            sound.status = SoundStatus.objects.get(id=1)
            sound.save()
            return redirect('/cashier')


class Dj(View):
    @shiftDecoration
    def get(self, request):
        if request.user.groups.filter(name="djs").exists():
            data = {'wait_mod': Sounds.objects.filter(status=2),
                    'pay_sounds': Sounds.objects.filter(status=1),
                    'post_sounds': Sounds.objects.filter(status=4).order_by('-id')[:5:-1],
                    'post_sounds_count': Sounds.objects.filter(status=4).count(),
                    'playForm': PlayForm()
                    }
            return render(request, 'clubbisenes/dj.html', data)
        else:
            return redirect('/test')


class DjPlay(View):
    @shiftDecoration
    def get(self, request, pk):
        if request.user.groups.filter(name="djs").exists():
            sound = Sounds.objects.get(id=pk)
            sound.status = SoundStatus.objects.get(id=4)
            sound.save()
            data = {'wait_mod': Sounds.objects.filter(status=2),
                    'pay_sounds': Sounds.objects.filter(status=1),
                    'post_sounds': Sounds.objects.filter(status=4).order_by('-id')[:5:-1],
                    'post_sounds_count': Sounds.objects.filter(status=4).count(),
                    'playForm': PlayForm()
                    }

            return redirect('clubbisenes/dj.html')
        else:
            return redirect('/test')


class SoundModerationView(View):
    @shiftDecoration
    def get(self, request, pk):
        if request.user.groups.filter(name="djs").exists():
            product = Sounds.objects.get(id=pk)
            productModerForm = ModerationForm()
            return render(request, 'clubbisenes/product.html',
                          {'product': product, 'productModerForm': productModerForm})
        else:
            return redirect('/test')

    def post(self, request, pk):
        form = ModerationForm(request.POST)
        if form.is_valid():

            moderation = form.cleaned_data.get('mod')
            if moderation == 'Y':
                sound = Sounds.objects.get(id=pk)
                sound.status = SoundStatus.objects.get(id=3)
                sound.save()
            else:

                sound = Sounds.objects.get(id=pk)
                sound.status = SoundStatus.objects.get(id=5)
                sound.save()
        return redirect('/dj')


class bdFull(View):
    def get(self):
        for table in range(1, 41):
            new_table = Table()
            new_table.number = table
            new_table.save()
            for user in range(1, 7):
                user_name = "table-{0}_user-{1}".format(table, user)
                new_user = User.objects.create_user(username=user_name, password="12345")
                new_user.save()
                user_profile = UserProfileModel()
                user_profile.user = new_user
                user_profile.table = new_table
                user_profile.save()

        return redirect('/')

class DeleteShift(View):
    @shiftDecoration
    def get(self, request):
        if request.user.groups.filter(name="cachers").exists():
            shift = ShiftUser.objects.get(state=True).delete()
            return redirect('/cashier')
        else:
            return redirect('/test')

class OpenShift(View):
    def get(self, request):
        if request.user.groups.filter(name="cachers").exists():
            shift = ShiftUser()
            shift.save()
            day_password = shift.day_password
            users = User.objects.all()
            for user in users:
                if user.groups.filter(name="cachers").exists() or user.groups.filter(name="djs").exists() :
                    continue
                else:
                    user.password = '12345'
                    user.save()
            return redirect('/cashier')
        else:
            return redirect('/test')
