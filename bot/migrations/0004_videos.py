# Generated by Django 4.2.3 on 2023-08-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_remove_user_first_name_remove_user_is_register_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('video_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
