from django_filters import rest_framework as filters 
from user.models import User 

class UserFilter(filters.FilterSet):
    """
    This class is used for filtering users based on fields like category.
    """
    category = filters.CharFilter(field_name="category")

    class Meta:
        model = User  # Define the model to filter
        fields = ['category']  # Fields available for filtering