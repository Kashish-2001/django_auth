# Generated by Django 3.2.8 on 2021-10-15 20:25

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.models.MyUserManager()),
            ],
        ),
    ]
