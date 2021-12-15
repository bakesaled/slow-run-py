from django.db.models import fields
from rest_framework import serializers
from activities.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'name', 'upload_id', 'type', 'distance',
                  'moving_time', 'average_speed', 'max_speed', 'total_elevation_gain', 'start_date_local', 'start_time_local', 'has_heartrate',
                  'average_heartrate',
                  'max_heartrate',
                  'average_watts',
                  'max_watts',
                  'kilojoules',
                  'elev_high',
                  'elev_low',)
