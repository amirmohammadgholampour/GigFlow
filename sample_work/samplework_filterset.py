from django_filters import rest_framework as filters 
from sample_work.models import SampleWork 

class SampleWorkFilter(filters.FilterSet):
    """
    FilterSet for SampleWork model.
    
    Provides filtering capabilities for sample work projects based on skills.
    This allows clients to search for sample works that match specific skills.
    """
    skill = filters.CharFilter(field_name="skill", lookup_expr="icontains")

    class Meta:
        model = SampleWork 
        fields = ["skill"]