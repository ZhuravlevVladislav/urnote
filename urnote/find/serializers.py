from rest_framework import serializers


class MillisecondsSerializer(serializers.Serializer):
    times = serializers.ListField(
        child=serializers.IntegerField()
    )
