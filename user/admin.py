from django.contrib import admin
from user.models import User

# Registering the User model to the Django admin interface with customizations
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Specifies the fields to be displayed in the admin list view
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'phone_number', 'category__name', 'resume']
    
    # Specifies the fields that will be clickable links in the admin list view
    list_display_links = ['username']
    
    # Adds filters in the admin list view for easy searching by category or user type
    list_filter = ['category__name', 'user_type']
    
    # Sets the number of entries per page in the admin list view
    list_per_page = 10 
    
    # Orders the entries by username
    ordering = ['username']
    
    # Specifies the fields to be searched in the admin interface
    search_fields = ['username', 'email', 'phone_number']
