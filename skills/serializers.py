from skills.models import Skill
from rest_framework import serializers

# Serializer to handle the serialization of Skill model data
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        # Defines the fields to be included in the skill serializer
        fields = ["name", "category"]
