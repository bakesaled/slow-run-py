# Generated by Django 3.2.9 on 2022-01-21 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extern_id', models.BigIntegerField(default=0)),
                ('name', models.CharField(default='', max_length=200)),
                ('upload_id', models.BigIntegerField()),
                ('type', models.CharField(default='', max_length=50)),
                ('distance', models.FloatField(default=0)),
                ('moving_time', models.FloatField(default=0)),
                ('average_speed', models.FloatField(default=0)),
                ('max_speed', models.FloatField(default=0)),
                ('total_elevation_gain', models.FloatField(default=0)),
                ('start_date', models.DateTimeField()),
                ('timezone', models.CharField(default='', max_length=200)),
                ('utc_offset', models.IntegerField(default=0)),
                ('has_heartrate', models.BooleanField(default=False)),
                ('average_heartrate', models.FloatField(null=True)),
                ('max_heartrate', models.FloatField(null=True)),
                ('average_watts', models.FloatField(null=True)),
                ('max_watts', models.FloatField(null=True)),
                ('kilojoules', models.FloatField(null=True)),
                ('elev_high', models.FloatField(default=0)),
                ('elev_low', models.FloatField(default=0)),
            ],
        ),
    ]
