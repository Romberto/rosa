# Generated by Django 3.2 on 2021-06-11 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubbisenes', '0016_alter_userprofilemodel_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shiftuser',
            name='day_password',
        ),
    ]