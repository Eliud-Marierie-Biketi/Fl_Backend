# Generated by Django 5.1.3 on 2024-11-10 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='subscription_end_date',
            field=models.DateField(default=datetime.date(2024, 12, 16)),
        ),
    ]
