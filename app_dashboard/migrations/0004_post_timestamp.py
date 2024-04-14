# Generated by Django 5.0.4 on 2024-04-13 14:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_dashboard', '0003_remove_post_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
