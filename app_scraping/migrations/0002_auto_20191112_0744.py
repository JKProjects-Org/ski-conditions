# Generated by Django 2.2.6 on 2019-11-12 07:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_scraping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skiresort',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 12, 7, 44, 56, 812362, tzinfo=utc)),
        ),
    ]
