from rest_framework.routers import DefaultRouter
from core.views import RepositoryViewSet

app_name = 'core'

router = DefaultRouter(trailing_slash=False)
router.register(r'searchGit', RepositoryViewSet, basename='searchGit')

urlpatterns = router.urls
