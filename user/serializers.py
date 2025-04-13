from rest_framework import serializers
from user.models import User

# Serializer for serializing user data (retrieving and updating user information)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Defines the fields to be included in the user serializer
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'user_type', 'category', 'phone_number', 'resume']