"""
Category API View

This module provides CRUD API endpoints for managing categories using Django REST Framework's ModelViewSet.
It supports:
- Listing all categories (GET)
- Retrieving a specific category (GET by ID)
- Creating new categories (POST)
- Updating existing categories (PUT/PATCH)
- Deleting categories (DELETE)

Permissions:
- Read operations (GET) are open to all users.
- Write operations (POST, PUT, DELETE) are restricted to admin users only.

Features:
- Paginated responses using a custom pagination class
- Permission enforcement via IsAdminOrReadOnly class
"""
# Import necessary serializer, model for handling project data.
from category.models import Category 
from category.serializers import CategorySerializer 

# Import custom pagination class for handling paginated responses.
from core.pagination import CustomPageNumberPagination

# Import permission from core folder.
from core.permissions import IsAdminOrReadOnly 

# Import viewset from rest_framework module
from rest_framework import viewsets

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all() # give all category from Database
    serializer_class = CategorySerializer 
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAdminOrReadOnly] # this permission shows `if user not is_admin return category but normal users can not POST, DELETE and updated category`