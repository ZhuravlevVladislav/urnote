from rest_framework import serializers

class RhythmDataSerializer(serializers.Serializer):
    rhythm_data = serializers.ListField(
        child=serializers.IntegerField()
    )
