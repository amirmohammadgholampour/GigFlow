# Import the admin module from django.contrib to register models in the Django admin interface
from django.contrib import admin 

# Import the Projects model to register it with the Django admin
from projects.models import Projects

# Register the Projects model with custom admin options
@admin.register(Projects)
class ProjectAdmin(admin.ModelAdmin):
    # Specifies the fields to be displayed in the admin list view
    list_display = ['user__username', 'name', 'description', 'category__name', 'deadline', 'price', 'created_at']  
    
    # Specifies the fields that will be clickable links in the admin list view
    list_display_links = ['user__username']  
    
    # Sets the number of entries per page in the admin list view
    list_per_page = 10     
    
    # Adds a filter for the 'category__name' field in the admin list view
    list_filter = ['category__name'] 
    
    # Orders the entries by name and category
    ordering = ['name', 'category'] 
    
    # Specifies the fields to be searched in the admin interface
    search_fields = ['name']
