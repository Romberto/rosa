# Generated by Django 3.2 on 2021-04-20 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubbisenes', '0005_auto_20210420_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sounds',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]