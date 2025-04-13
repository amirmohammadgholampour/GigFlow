"""
SkillView:
API endpoint that allows skills to be viewed or edited.

Actions:
- list:    Returns a paginated list of all skills.
- retrieve:Returns a single skill instance.
- create:  Creates a new skill (admin only).
- update:  Updates an existing skill (admin only).
- partial_update: Partially updates a skill (admin only).
- destroy: Deletes a skill (admin only).

Permissions:
- Safe methods (GET, HEAD, OPTIONS) are open to all users.
- Unsafe methods (POST, PUT, PATCH, DELETE) are restricted to admin users.

Pagination:
- Uses CustomPageNumberPagination to paginate results.
"""

# Import necessary serializers, models for handling project data.
from skills.models import Skill 
from skills.serializers import SkillSerializer

# Import permission from core folder.
from core.permissions import IsAdminOrReadOnly

# Import custom pagination class for handling paginated responses.
from core.pagination import CustomPageNumberPagination

# Import viewset from rest_framework module.
from rest_framework import viewsets 

class SkillView(viewsets.ModelViewSet):
    queryset = Skill.objects.all() # give all skills from Database
    serializer_class = SkillSerializer 
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAdminOrReadOnly] # this permission shows `if user not is_admin return category but normal users can not POST, DELETE and updated category`