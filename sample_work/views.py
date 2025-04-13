"""
Sample Work Views Module

This module contains API views for managing sample work projects for freelancers.
It provides endpoints for creating, retrieving, updating, and deleting sample work
projects, as well as filtering and searching capabilities.

Classes:
    SampleWorkFilter: FilterSet for filtering sample work projects
    SampleWorkView: Main API view for sample work CRUD operations
"""

# Import necessary serializers, models for handling project data.
from sample_work.models import SampleWork 
from sample_work.serializers import SampleWorkSerializer 

# Import API class for creating custom views. 
from rest_framework.views import APIView

# Import Responses and status from rest_framework to handle HTTP responses and status codes.
from rest_framework.response import Response 
from rest_framework import status 

from sample_work.samplework_filterset import SampleWorkFilter
from core.pagination import CustomPageNumberPagination 

# Import swagger utilities for API documentation generation.
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi 

class SampleWorkView(APIView):
    """
    API view for handling sample work operations.
    
    This view provides endpoints for:
    - Listing and filtering sample work projects (GET)
    - Creating new sample work projects (POST)
    - Updating existing sample work projects (PUT)
    - Deleting sample work projects (DELETE)
    
    All operations except GET require authentication, and certain operations
    are restricted to freelancers who own the sample work projects.
    """
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'id',
                    openapi.IN_QUERY,
                    description="Enter ID of sample project",
                    type=openapi.TYPE_INTEGER
                ),
                openapi.Parameter(
                    'search',
                    openapi.IN_QUERY,
                    description="Enter username of freelancer",
                    type=openapi.TYPE_STRING 
                )
            ]
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of sample work projects with optional filtering.
        
        This endpoint allows clients to:
        - Retrieve all sample work projects
        - Filter projects by ID, username, name, or skills
        - Search for projects by username
        - Paginate results
        
        Parameters:
            request (Request): The HTTP request object
            
        Returns:
            Response: A paginated list of sample work projects matching the criteria
        """
        queryset = SampleWork.objects.all() 

        search_query = request.GET.get("search", None) 
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        filter_sample_work = SampleWorkFilter(request.GET, queryset=queryset)
        queryset = filter_sample_work.qs 

        if self.pagination_class:
            paginator = self.pagination_class()
        else:
            paginator = None 
        
        if paginator:
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = SampleWorkSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = SampleWorkSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=SampleWorkSerializer,
        responses={
            status.HTTP_201_CREATED: SampleWorkSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data",
            status.HTTP_401_UNAUTHORIZED: "Authentication required",
            status.HTTP_403_FORBIDDEN: "You do not have permission"
        }
    )
    def post(self, request):
        """
        Create a new sample work project.
        
        This endpoint allows freelancers to create new sample work projects.
        Only authenticated freelancers can create sample work projects.
        
        Parameters:
            request (Request): The HTTP request object containing sample work data
            
        Returns:
            Response: The created sample work project data or error details
            
        Status Codes:
            201: Sample work project created successfully
            400: Invalid data provided
            401: User is not authenticated
            403: User is not a freelancer
        """
        user = request.user 

        if not user.is_authenticated:
            return Response(
                {"detail":"Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.user_type != "freelancer":
            return Response(
                {"detail":"Only freelancers can create sample projects"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = SampleWorkSerializer(data=request.data) 

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(
                {"detail":"Sample project created successfully!", "data":serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"detail":"Invalid data", "errors":serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'sample_project_id',
                openapi.IN_QUERY,
                description="Enter SampleProject ID to delete it",
                type=openapi.TYPE_INTEGER 
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: "SampleProject deleted successfully!",
            status.HTTP_401_UNAUTHORIZED: "Authentication required",
            status.HTTP_404_NOT_FOUND: "SampleProject not found",
            status.HTTP_403_FORBIDDEN: "You are not allowed to delete this sample project"
        }
    )
    def delete(self, request):
        """
        Delete a sample work project.
        
        This endpoint allows freelancers to delete their own sample work projects.
        Only the owner of a sample work project can delete it.
        
        Parameters:
            request (Request): The HTTP request object with sample_project_id parameter
            
        Returns:
            Response: Success message or error details
            
        Status Codes:
            204: Sample work project deleted successfully
            401: User is not authenticated
            403: User is not a freelancer or not the owner
            404: Sample work project not found
        """
        user = request.user 

        if not user.is_authenticated:
            return Response(
                {"detail":"Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if user.user_type != "freelancer":
            return Response(
                {"detail":"Only freelancers can delete their sample projects"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        samplework_id = request.GET.get("sample_project_id")
        
        try:
            sample_work = SampleWork.objects.get(id=samplework_id, user=user) 
        except SampleWork.DoesNotExist:
            return Response(
                {"detail":"Sample project not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        sample_work.delete()

        return Response(
            {"detail":"Sample project deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'sample_project_id',
                openapi.IN_QUERY,
                description="Enter sample project ID to update this",
                type=openapi.TYPE_INTEGER
            )
        ],
        request_body=SampleWorkSerializer,
        response={
            status.HTTP_200_OK: SampleWorkSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data",
            status.HTTP_404_NOT_FOUND: "SampleProject not found",
            status.HTTP_401_UNAUTHORIZED: "Authentication required",
            status.HTTP_403_FORBIDDEN: "You are not allowed to update this sample work"
        }
    )
    def put(self, request):
        """
        Update an existing sample work project.
        
        This endpoint allows freelancers to update their own sample work projects.
        Only the owner of a sample work project can update it.
        
        Parameters:
            request (Request): The HTTP request object with sample_project_id parameter
                              and updated sample work data
            
        Returns:
            Response: Updated sample work project data or error details
            
        Status Codes:
            200: Sample work project updated successfully
            400: Invalid data provided
            401: User is not authenticated
            403: User is not the owner of the sample work
            404: Sample work project not found
        """
        user = request.user 

        if not user.is_authenticated:
            return Response(
                {"detail":"Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get the sample_project_id from the request
        samplework_id = request.GET.get("sample_project_id")
        if not samplework_id:
            return Response(
                {"detail":"sample_project_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to get the sample work object
        try:
            sample_work = SampleWork.objects.get(id=samplework_id) 
        except SampleWork.DoesNotExist:
            return Response(
                {"detail":"Sample project not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if the user is the owner
        if sample_work.user != user:
            return Response(
                {"detail":"You can only update your own sample projects"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = SampleWorkSerializer(sample_work, data=request.data, partial=True) 

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail":"Sample project updated successfully!", "data":serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail":"Invalid data", "errors":serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )