from api.views import MixtapeViewSet
from rest_framework import routers
from api import views as api_views

router = routers.DefaultRouter()
router.register('mixtapes',api_views.MixtapeViewSet)