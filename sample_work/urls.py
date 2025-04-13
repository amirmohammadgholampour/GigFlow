from django.urls import path 
from sample_work.views import SampleWorkView 

urlpatterns = [
    path("", SampleWorkView.as_view())
]
