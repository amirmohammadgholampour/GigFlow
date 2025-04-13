from django.urls import path 
from projects.views import ProjectsView 

urlpatterns = [
    path("", ProjectsView.as_view())    
]