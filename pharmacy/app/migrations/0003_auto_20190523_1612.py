# Generated by Django 2.2.1 on 2019-05-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snizenje',
            name='iznos',
            field=models.IntegerField(max_length=10),
        ),
    ]