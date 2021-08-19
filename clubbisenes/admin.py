from django.contrib import admin
from clubbisenes.models import SoundStatus, Sounds, UserProfileModel, ShiftUser
from django.contrib.auth.models import User


@admin.register(SoundStatus)
class AdminSoundStatus(admin.ModelAdmin):
    list_display = ('id', 'statusName')


@admin.register(UserProfileModel)
class AdminProfileUser(admin.ModelAdmin):
    list_display = ('user', 'table', 'activate')


@admin.register(ShiftUser)
class AdminShift(admin.ModelAdmin):
    list_display = ('state', 'date_open', 'date_close')


admin.site.register(Sounds)
