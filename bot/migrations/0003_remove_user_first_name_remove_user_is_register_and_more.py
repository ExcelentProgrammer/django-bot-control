# Generated by Django 4.2.3 on 2023-07-27 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_user_left_chanels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_register',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='left_chanels',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='status',
        ),
    ]