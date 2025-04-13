from rest_framework import serializers
from category.models import Category

# Serializer to handle the serialization of Category model data
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # Defines the fields to be included in the category serializer
        fields = ['name', 'created_at']
