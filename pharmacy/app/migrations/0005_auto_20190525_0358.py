# Generated by Django 2.2.1 on 2019-05-25 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190524_0259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='ime',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='prezime',
        ),
    ]
