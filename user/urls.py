from .views import UserView
from django.urls import path 

urlpatterns = [
    path('', UserView.as_view()),
]