from django.contrib import admin
from clubbisenes.models import SoundStatus, Sounds, Table, UserProfileModel, ShiftUser


# admin.site.register(SoundStatus)


@admin.register(SoundStatus)
class AdminSoundStatus(admin.ModelAdmin):
    list_display = ('id', 'statusName')


@admin.register(UserProfileModel)
class AdminProfileUser(admin.ModelAdmin):
    list_display = ('user', 'table', 'activate')


@admin.register(ShiftUser)
class AdminShift(admin.ModelAdmin):
    list_display = ('state', 'date_open', 'date_close','day_password')


admin.site.register(Sounds)

admin.site.register(Table)
