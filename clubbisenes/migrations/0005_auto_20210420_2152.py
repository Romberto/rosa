# Generated by Django 3.2 on 2021-04-20 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubbisenes', '0004_auto_20210420_2114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sounds',
            options={'verbose_name': 'Заказ песни', 'verbose_name_plural': 'Заказы песен'},
        ),
        migrations.AddField(
            model_name='sounds',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
