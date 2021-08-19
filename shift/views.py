import datetime


from django.shortcuts import render, redirect
from django.views import View

from clubbisenes.models import ShiftUser, UserProfileModel, Sounds
from clubbisenes.views import shiftDecoration


class CloseShiftView(View):
    @shiftDecoration
    def get(self, request):
        if request.user.groups.filter(name="cachers").exists():
            shift_day = ShiftUser.objects.get(state=True)
            shift_day.state = False
            close_time = datetime.datetime.now()
            shift_day.date_close = close_time
            shift_day.save()
            tables = UserProfileModel.objects.all()
            sounds = Sounds.objects.all()
            for table in tables:
                table.delete()
            for sound in sounds:
                sound.delete()
            return redirect('/cashier')
        else:
            return redirect('/test')


class OpenShiftView(View):
    def get(self, request):
        if request.user.groups.filter(name="cachers").exists():
            shift = ShiftUser()
            shift.save()
            return redirect('/cashier')
        else:
            return redirect('/test')
