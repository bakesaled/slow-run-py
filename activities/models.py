from django.db import models

# Create your models here.


class Activity(models.Model):
    #'name', 'upload_id', 'type', 'distance', 'moving_time',
    # 'average_speed', 'max_speed', 'total_elevation_gain',
    # 'start_date_local'
    name = models.CharField(max_length=200, blank=False, default='')
    upload_id = models.BigIntegerField(blank=False)
    type = models.CharField(max_length=50, blank=False, default='')
    distance = models.FloatField(blank=False, default=0)
    moving_time = models.FloatField(blank=False, default=0)
    average_speed = models.FloatField(blank=False, default=0)
    max_speed = models.FloatField(blank=False, default=0)
    total_elevation_gain = models.FloatField(blank=False, default=0)
    start_date_local = models.DateField(blank=False)
    start_time_local = models.DateTimeField(blank=False)
    has_heartrate = models.BooleanField(blank=False, default=False)
    average_heartrate = models.FloatField(blank=False, default=0)
    max_heartrate = models.FloatField(blank=False, default=0)
    average_watts = models.FloatField(blank=False, default=0)
    max_watts = models.FloatField(blank=False, default=0)
    kilojoules = models.FloatField(blank=False, default=0)
    elev_high = models.FloatField(blank=False, default=0)
    elev_low = models.FloatField(blank=False, default=0)
