from django.db.models import fields
from rest_framework import serializers
from activities.models import Activity
from datetime import datetime as dt


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'extern_id', 'name', 'upload_id', 'type', 'distance',
                  'moving_time', 'average_speed', 'max_speed', 'total_elevation_gain', 'start_date_local', 'start_time_local', 'has_heartrate',
                  'average_heartrate',
                  'max_heartrate',
                  'average_watts',
                  'max_watts',
                  'kilojoules',
                  'elev_high',
                  'elev_low',)


class StravaActivitySerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        extern_id = data.get('id')
        name = data.get('name')
        upload_id = data.get('upload_id')
        type = data.get('type')
        distance = data.get('distance')
        moving_time = data.get('moving_time')
        average_speed = data.get('average_speed')
        max_speed = data.get('max_speed')
        total_elevation_gain = data.get('total_elevation_gain')
        start_date_local = dt.strptime(
            data.get('start_date_local'), '%Y-%m-%dT%H:%M:%S%z')
        start_time_local = dt.strptime(
            data.get('start_date_local'), '%Y-%m-%dT%H:%M:%S%z')
        has_heartrate = data.get('has_heartrate')
        average_heartrate = data.get('average_heartrate')
        max_heartrate = data.get('max_heartrate')
        average_watts = data.get('average_watts')
        max_watts = data.get('max_watts')
        kilojoules = data.get('kilojoules')
        elev_high = data.get('elev_high')
        elev_low = data.get('elev_low')

        return {
            'extern_id': extern_id,
            'name': name,
            'upload_id': upload_id,
            'type': type,
            'distance': distance,
            'moving_time': moving_time,
            'average_speed': average_speed,
            'max_speed': max_speed,
            'total_elevation_gain': total_elevation_gain,
            'start_date_local': start_date_local,
            'start_time_local': start_time_local,
            'has_heartrate': has_heartrate,
            'average_heartrate': average_heartrate,
            'max_heartrate': max_heartrate,
            'average_watts': average_watts,
            'max_watts': max_watts,
            'kilojoules': kilojoules,
            'elev_high': elev_high,
            'elev_low': elev_low
        }

    def create(self, validated_data):
        return Activity.objects.create(**validated_data)
