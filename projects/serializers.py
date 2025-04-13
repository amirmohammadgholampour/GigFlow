from projects.models import Projects
from rest_framework import serializers

# Serializer to handle the serialization of Project model data
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        # Defines the fields to be included in the project serializer
        fields = ['user', 'name', 'description', 'category', 'deadline', 'price', 'created_at']
