from skills.views import SkillView 
from rest_framework.routers import DefaultRouter 

router = DefaultRouter()
router.register(r'', SkillView, basename="SkillViewSet")

urlpatterns = router.urls