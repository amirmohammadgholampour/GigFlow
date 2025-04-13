from rest_framework import serializers
from sample_work.models import SampleWork

# Serializer to handle the serialization of SampleWork model data
class SampleWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleWork
        # Defines the fields to be included in the sample work serializer
        fields = ['user', 'name', 'description', 'skill', 'image', 'created_at']