from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import SoundForms, ModerationForm, PlayForm, PayForm, AuthForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


def shiftDecoration(func):
    def wraper(self, request):
        shistState = ShiftUser.objects.filter(state=True)
        if not shistState:
            return redirect('/shift')
        return func(self, request)

    return wraper

    return wraper


class ShiftError(View):
    def get(self, request):
        return render(request, 'clubbisenes/shifterror.html')


class Authenticate(View):
    @shiftDecoration
    def get(self, request):
        _username = request.user.username
        user = User.objects.get(username=_username)
        print(user.profile.get().table)
        table = user.profile.get().table
        data = {'user': user.username,
                'table': table,
                'sounds': Sounds.objects.filter(status=4).order_by('-id')[:3:-1],
                'wait_mod': Sounds.objects.filter(status=2).order_by('-id')[:3:-1]
                }
        return render(request, 'clubbisenes/index.html', data)


class Main(View):
    @shiftDecoration
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(name="clients").exists():
                try:
                    user = UserProfileModel.objects.get(user=request.user)
                    table = user.table
                    data = {
                        'table': table,
                        'sounds': Sounds.objects.filter(status=4).order_by('-id')[:3:-1],
                        'wait_mod': Sounds.objects.filter(status=2).order_by('-id')[:3:-1]
                    }
                    return render(request, 'clubbisenes/index.html', data)
                except ObjectDoesNotExist:
                    return redirect('reg/changeTable/')
            else:
                return redirect('/reg/login/')
        else:
            return redirect('/reg/login/')


class Test(View):
    def get(self, request):
        return render(request, 'clubbisenes/test.html', {})


class Sound(View):
    @shiftDecoration
    def get(self, request):
        if request.user.is_authenticated:
            sound_form = SoundForms(request.POST or None)

            try:
                number = request.user.profile.get().table
            except:
                return redirect('/reg/changeTable')
            return render(request, 'clubbisenes/sound.html', {'sound_form': sound_form, 'number': number})
        else:
            return redirect('/reg/login/')

    def post(self, request):
        form = SoundForms(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            new_sound = Sounds(**data)
            new_sound.user = request.user
            new_sound.save()
            return redirect('/auth')
        else:
            return redirect('/login/')


class LogIn(View):
    def get(self, request):
        form = AuthForm(request.POST or None)
        data = {
            'AuthForm': form,
            'error': form.errors

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
                return redirect('/logIn/')


class Cashier(View):
    def get(self, request):
        if request.user.groups.filter(name="cachers").exists():
            all_profile = UserProfileModel.objects.all().order_by('table')
            table_list = []
            for table in all_profile:
                number = table.table
                if number in table_list:
                    continue
                else:
                    table_list.append(number)

            data = {'wait_pay': Sounds.objects.filter(status=3),
                    'table_list': table_list,
                    'payForm': PayForm(),
                    'state': ShiftUser.objects.filter(state=True),
                    'post_sounds_count': Sounds.objects.filter(status=4).count()}
            return render(request, 'clubbisenes/cashier.html', data)
        else:
            return redirect('/test')

    def post(self, requests):
        if requests.user.groups.filter(name="cachers").exists():
            form = PayForm(requests.POST)
            if form.is_valid():
                soundId = form.cleaned_data.get('pay')
                sound = Sounds.objects.get(id=int(soundId))
                sound.status = SoundStatus.objects.get(id=1)
                sound.save()
                return redirect('/cashier')
            else:
                print('ooo')


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

            return render(request, 'clubbisenes/dj.html', data)
        else:
            return redirect('/test')


class SoundModerationView(View):

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


class Dynamic_wait_mod(View):

    def get(self, request):
        lastItemId = request.GET.get('lastId')
        filters = {
            'status': 2
        }
        filter__pk = 'pk__gt=int(lastItemId)'
        print(lastItemId)
        try:
            wait_mod = Sounds.objects.filter(pk__gt=int(lastItemId))

        except TypeError:
            return JsonResponse({'data': False})
        if not wait_mod:
            return JsonResponse({'data': False})
        data=[]
        for sound in wait_mod:
            obj = {
                'id': sound.id,
                'table': sound.table,
                'name': sound.name
            }
            data.append(obj)
        data[-1]['last_item'] = True
        return JsonResponse({'data': data})
