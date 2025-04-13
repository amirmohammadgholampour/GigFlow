from django_filters import rest_framework as filters 
from projects.models import Projects 

class ProjectsFilter(filters.FilterSet):
    """
    This class defines filters for the 'Projects' model, allowing users to filter projects 
    based on name and category. The filters use 'icontains' lookup to perform case-insensitive 
    partial matching.

    Fields:
        name (CharFilter): Filters projects by name with case-insensitive matching.
        category (CharFilter): Filters projects by category with case-insensitive matching.
    """
    
    # Filter for project name using partial, case-insensitive matching
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    
    # Filter for project category using partial, case-insensitive matching
    category = filters.CharFilter(field_name="category")

    class Meta:
        # Link the filter to the Projects model
        model = Projects
        # Define the fields that can be filtered
        fields = ["name", "category"]