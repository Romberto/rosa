import datetime

from django.shortcuts import render, redirect
from django.views import View

from clubbisenes.models import ShiftUser
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
