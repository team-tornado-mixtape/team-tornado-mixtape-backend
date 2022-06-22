from api.views import MixtapeViewSet,UserViewSet
from rest_framework import routers
from rest_framework_nested import routers
from api import views as api_views


router = routers.DefaultRouter()
router.register('mixtapes',api_views.MixtapeViewSet)
router.register('users',api_views.UserViewSet,basename='users')
users_router = routers.NestedSimpleRouter(router,'users', lookup='user')
users_router.register(
    'profiles',
    api_views.ProfileView,
    basename='profiles',
)
