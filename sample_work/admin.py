# Import the admin module from django.contrib to register models in the Django admin interface
from django.contrib import admin 

# Import the SampleWork model to register it with the Django admin
from sample_work.models import SampleWork

# Register the SampleWork model with custom admin options
@admin.register(SampleWork)
class SampleWorkAdmin(admin.ModelAdmin):
    # Specifies the fields to be displayed in the admin list view
    list_display = ['user__username', 'name', 'description', 'skill', 'image']
    
    # Specifies the fields that will be clickable links in the admin list view
    list_display_links = ['user__username']
    
    # Sets the number of entries per page in the admin list view
    list_per_page = 10 
    
    # Adds a filter for the 'skill' field in the admin list view
    list_filter = ['skill'] 
    
    # Orders the entries by the 'skill' field
    ordering = ['skill']
    
    # Specifies the fields to be searched in the admin interface
    search_fields = ['name']
