# Generated by Django 3.0.5 on 2020-05-03 17:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('challengeApp', '0011_analyticsaccount_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='logevents',
            name='timeresponse',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]