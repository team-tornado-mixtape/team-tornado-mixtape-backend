from api.views import MixtapeViewSet,UserView
from rest_framework import routers
from rest_framework_nested import routers
from api import views as api_views


router = routers.DefaultRouter()
router.register('mixtapes',api_views.MixtapeViewSet)
router.register('users',api_views.UserViewSet)