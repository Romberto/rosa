# Generated by Django 3.2 on 2021-04-20 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubbisenes', '0006_alter_sounds_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Номер стола',
                'verbose_name_plural': 'Номера столов',
            },
        ),
        migrations.AddField(
            model_name='sounds',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clubbisenes.table'),
        ),
    ]