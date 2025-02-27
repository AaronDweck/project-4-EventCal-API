from rest_framework import serializers
from ..models import Event

class EventSerializer(serializers.ModelSerializer):
    def validate(self, data):
        data['start_date'] = data['start_date'].replace(second=0, microsecond=0)
        data['end_date'] = data['end_date'].replace(second=0, microsecond=0)

        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError('End date is before the start date')

        return data

    class Meta:
        model = Event
        fields = '__all__'