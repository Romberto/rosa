from django.db import models
from django.contrib.auth.models import User
from random import randint


class Table(models.Model):
    number = models.IntegerField()

    def __str__(self):
        number = str(self.number)
        return number

    class Meta:
        verbose_name = "Номер стола"
        verbose_name_plural = "Номера столов"

class SoundStatus(models.Model):
    statusName = models.CharField(max_length=50)

    def __str__(self):
        return self.statusName

    class Meta:
        verbose_name = "Статусы песни"
        verbose_name_plural = "Статус песен"


class Sounds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=230)
    file = models.FileField(upload_to='files/', null=True , blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(SoundStatus, default=2, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заказ песни"
        verbose_name_plural = "Заказы песен"


class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    table = models.IntegerField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    activate = models.BooleanField(default=False)
    class Meta:
        verbose_name = "ProfileUser"
        verbose_name_plural = "ProfileUser"

class ShiftUser(models.Model):
    state = models.BooleanField(default=True)
    date_open = models.DateTimeField(auto_now_add=True)
    date_close = models.DateTimeField(blank=True, null=True)

