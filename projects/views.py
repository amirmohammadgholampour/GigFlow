"""
Projects API View

This module provides API endpoints for managing projects, including:
- Retrieving a list of projects (GET)
- Creating new projects (POST)
- Updating existing projects (PUT)
- Deleting projects (DELETE)

All operations enforce authentication and role-based permissions:
- Only authenticated users of type 'employer' can create, update, or delete projects.
- Projects can only be modified or deleted by their owner.

Additional features:
- Filtering projects using query parameters (e.g., project_id, name, search)
- Paginated responses using a custom pagination class
- Swagger documentation for API discoverability

Endpoints:
- GET: List projects with optional filtering and pagination
- POST: Create a new project (employer only)
- PUT: Update an existing project (owner only)
- DELETE: Remove a project (owner only)
"""
# Import necessary serializers, models for handling project data.
from projects.serializers import ProjectSerializer
from projects.models import Projects 

# Import project filter from project_filterset app.
from projects.project_filterset import ProjectsFilter

# Import APIView class for creating custom views.
from rest_framework.views import APIView

# Import Response and status from rest_framework to handle HTTP responses and status codes.
from rest_framework.response import Response
from rest_framework import status

# Import Swagger utilities for API documentation generation.
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi 

# Import custom pagination class for handling paginated responses.
from core.pagination import CustomPageNumberPagination

class ProjectsView(APIView):
    """
    API view for handling CRUD operations (Create, Read, Update, Delete) for projects.
    Supports filtering, pagination, and different HTTP methods (GET, POST, DELETE, PUT).
    """
    
    # Set the custom pagination class to be used for this view
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'project_id',
                openapi.IN_QUERY,
                description="Enter project_ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="Enter name of project",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve a list of projects.
        Supports filtering by 'search' query parameter and pagination.
        """
        # Get all projects from the database
        queryset = Projects.objects.all()

        # Apply search filter if 'search' query parameter is provided
        search_query = request.GET.get("search", None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Apply additional filters using the ProjectsFilter class
        filter_projects = ProjectsFilter(request.GET, queryset=queryset)
        queryset = filter_projects.qs

        # Handle pagination if pagination class is set
        if self.pagination_class:
            paginator = self.pagination_class()
        else:
            paginator = None

        # If pagination is enabled, paginate the queryset
        if paginator:
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = ProjectSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # If no pagination, return all results
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=ProjectSerializer,
        responses={
            status.HTTP_201_CREATED: ProjectSerializer(), 
            status.HTTP_400_BAD_REQUEST: 'Invalid data',
            status.HTTP_403_FORBIDDEN: "You are Not allowed to delete other project",
            status.HTTP_401_UNAUTHORIZED: "Authenticated required"
        }
    )
    def post(self, request):
        """
        Handle POST request to create a new project.
        Only authenticated users of type 'employer' can create projects.
        """
        user = request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response(
                {"detail":"Authenticated required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Ensure the user is an employer
        if user.user_type == "freelancer":
            return Response(
                {"detail":"Just employers can create a project"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validate and save the new project using the serializer
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(
                {"detail":"Project create successfully!", "data":serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"detail":"Invalid data", "error":serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'project_id',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: "Project deleted successfully!",
            status.HTTP_404_NOT_FOUND: "Project not found",
            status.HTTP_403_FORBIDDEN: "You are Not allowed to delete other project",
            status.HTTP_401_UNAUTHORIZED: "Authenticated required"
        }
    )
    def delete(self, request):
        """
        Handle DELETE request to delete a project.
        Only the employer who created the project can delete it.
        """
        user = request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response(
                {"detail":"Authenticated required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Ensure the user is an employer
        if user.user_type != "employer":
            return Response(
                {"detail":"Just employers can delete projects"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get the project ID from the request
        project_id = request.GET.get("project_id")  

        # Ensure a project ID is provided
        if not project_id:
            return Response(
                {"detail": "Project ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to fetch the project by ID and check if it belongs to the authenticated user
        try:
            project = Projects.objects.get(id=project_id, user=user) 
        except Projects.DoesNotExist:
            return Response(
                {"detail": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the project
        project.delete()

        return Response(
            {"detail":"Project deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'project_id',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER
            )
        ], 
        request_body=ProjectSerializer,
        responses={
            status.HTTP_200_OK: ProjectSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data",
            status.HTTP_404_NOT_FOUND: "Project not found",
            status.HTTP_401_UNAUTHORIZED: "Authenticated required",
            status.HTTP_403_FORBIDDEN: "You do not have permission for update other project"
        }
    )
    def put(self, request):
        """
        Handle PUT request to update an existing project.
        Only the employer who created the project can update it.
        """
        user = request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get the project ID from the request
        project_id = request.GET.get("project_id")

        # Try to fetch the project by ID and check if it belongs to the authenticated user
        try:
            project = Projects.objects.get(id=project_id, user=user)
        except Projects.DoesNotExist:
            return Response(
                {"detail": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate and save the updated project using the serializer
        serializer = ProjectSerializer(project, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Project updated successfully!", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )