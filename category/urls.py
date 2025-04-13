from rest_framework.routers import DefaultRouter 
from category.views import CategoryView 

router = DefaultRouter()
router.register(r'', CategoryView, basename="CategoryViewSet")

urlpatterns = router.urls