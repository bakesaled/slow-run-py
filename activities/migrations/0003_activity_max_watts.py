# Generated by Django 3.2.9 on 2021-12-15 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20211215_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='max_watts',
            field=models.FloatField(default=0),
        ),
    ]