"""
User API View

This module provides API endpoints for user management operations including:
- Retrieving user information (GET)
- Creating new users (POST)
- Updating user information (PUT)
- Deleting user accounts (DELETE)

All endpoints enforce proper authentication and authorization to ensure users
can only access and modify their own data. The API uses Django REST Framework
for request handling and response formatting, with Swagger documentation for
API discoverability.

Endpoints:
- GET: Retrieve authenticated user's profile
- POST: Create a new user account (sign up)
- PUT: Update an existing user's information
- DELETE: Remove a user account

Authentication is required for all operations except user creation (POST).
"""
# Import necessary modules for creating API views and handling HTTP responses.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Import the User model to interact with the user data.
from user.models import User

# Import the serializer for the User model to serialize user data.
from user.serializers import UserSerializer

# Import custom pagination class for controlling pagination behavior in responses.
from core.pagination import CustomPageNumberPagination

# Import Swagger utilities for generating API documentation.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# View to handle user-related actions such as retrieving, creating, updating, and deleting a user
class UserView(APIView):
    pagination_class = CustomPageNumberPagination  # Custom pagination class for paginating responses

    # Handle GET request - Retrieve current authenticated user's data
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="User ID",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        user = request.user  # Get the currently authenticated user

        # If user is not authenticated, deny access
        if not user.is_authenticated:
            return Response(
                {"detail": "Please Sign-up"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        queryset = User.objects.all()  # Get all users

        queryset = queryset.filter(id=user.id)  # Filter to return only the requesting user

        paginator = self.pagination_class()  # Initialize custom pagination
        result_page = paginator.paginate_queryset(queryset, request)  # Apply pagination to the queryset
        serializer = UserSerializer(result_page, many=True)  # Serialize the paginated result

        return paginator.get_paginated_response(serializer.data)  # Return paginated response

    # Handle POST request - Register a new user
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            status.HTTP_201_CREATED: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                "Invalid data", 
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(type=openapi.TYPE_STRING),
                        "errors": openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            )
        }
    )
    def post(self, request):
        # Prevent already authenticated users from signing up again
        if request.user.is_authenticated:
            return Response(
                {"detail": "You cannot sign up because you already have an account."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = UserSerializer(data=request.data)  # Deserialize request data
        
        # If data is not valid, return error
        if not serializer.is_valid():
            return Response(
                {"detail": "Invalid data", "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST 
            )
        
        # Save new user to the database and hash password
        user = serializer.save()
        user.set_password(request.data.get("password"))  # Securely hash the password
        user.save()

        return Response(
            {"detail": "User created successfully! Now you have an account.", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    # Handle PUT request - Update authenticated user's data
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Enter a user_id to change data",
                required=False 
            )
        ],
        request_body=UserSerializer,
        response={
            status.HTTP_200_OK: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data",
            status.HTTP_401_UNAUTHORIZED: "Authentication required",
            status.HTTP_403_FORBIDDEN: "You do not have permission to update this user",
            status.HTTP_404_NOT_FOUND: "User not found"
        }
    )
    def put(self, request):
        user = request.user  # Get current authenticated user

        # Check if user is logged in
        if not user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get user_id from query parameters
        user_id = request.GET.get("user_id")

        if not user_id:
            return Response(
                {"detail": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to fetch the target user
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail":"User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Prevent users from updating others' profiles
        if int(user_id) != user.id: 
            return Response(
                {"detail": "You are not authorized to update this user."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = UserSerializer(user, data=request.data, partial=True)  # Allow partial updates
        
        if serializer.is_valid():
            serializer.save()  # Save updated user data
            return Response(
                {"detail": "User updated successfully!", "data": serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Handle DELETE request - Delete the authenticated user's account
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="User ID",
                type=openapi.TYPE_INTEGER  
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: "User deleted successfully",
            status.HTTP_401_UNAUTHORIZED: "Authentication required",
            status.HTTP_403_FORBIDDEN: "You do not have permission to delete this user",
            status.HTTP_404_NOT_FOUND: "User not found"
        }
    )
    def delete(self, request):
        user = request.user  # Get authenticated user

        # Require authentication
        if not user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get user ID from query params
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"detail": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to fetch the user to delete
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail":"User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Make sure user can delete only their own account
        if int(user_id) != user.id:
            return Response(
                {"detail": "You are not authorized to delete this user."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user.delete()  # Delete the user
        return Response(
            {"detail": "User deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )