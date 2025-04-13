# Import the admin module from django.contrib to register models in the Django admin interface
from django.contrib import admin 

# Import the Skill model to register it with the Django admin
from skills.models import Skill

# Register the Skill model with custom admin options
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    # Specifies the fields to be displayed in the admin list view
    list_display = ['name']
    
    # Sets the number of entries per page in the admin list view
    list_per_page = 10
