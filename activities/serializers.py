from django.db.models import fields
from rest_framework import serializers
from activities.models import Activity
from dateutil import parser


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'extern_id', 'name', 'upload_id', 'type', 'distance',
                  'moving_time', 'average_speed', 'max_speed', 'total_elevation_gain', 'start_date', 'timezone', 'utc_offset', 'has_heartrate',
                  'average_heartrate',
                  'max_heartrate',
                  'average_watts',
                  'max_watts',
                  'kilojoules',
                  'elev_high',
                  'elev_low',)


class StravaActivitySerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        existing_id = data.get('existing_id')
        id = None
        if existing_id and len(existing_id) > 0:
            id = existing_id
        extern_id = data.get('id')
        name = data.get('name')
        upload_id = data.get('upload_id')
        type = data.get('type')
        distance = data.get('distance')
        moving_time = data.get('moving_time')
        average_speed = data.get('average_speed')
        max_speed = data.get('max_speed')
        total_elevation_gain = data.get('total_elevation_gain')
        start_date = parser.parse(data.get('start_date'))
        utc_offset = data.get('utc_offset')
        timezone = data.get('timezone')
        has_heartrate = data.get('has_heartrate')
        average_heartrate = data.get('average_heartrate')
        max_heartrate = data.get('max_heartrate')
        average_watts = data.get('average_watts')
        max_watts = data.get('max_watts')
        kilojoules = data.get('kilojoules')
        elev_high = data.get('elev_high')
        elev_low = data.get('elev_low')

        return {
            'id': id,
            'extern_id': extern_id,
            'name': name,
            'upload_id': upload_id,
            'type': type,
            'distance': distance,
            'moving_time': moving_time,
            'average_speed': average_speed,
            'max_speed': max_speed,
            'total_elevation_gain': total_elevation_gain,
            'start_date': start_date,
            'utc_offset': utc_offset,
            'timezone': timezone,
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
