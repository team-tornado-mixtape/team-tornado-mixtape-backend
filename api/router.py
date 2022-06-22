from api.views import MixtapeViewSet,UserViewSet,ProfileViewSet
from rest_framework import routers
from rest_framework_nested import routers
from api import views as api_views


router = routers.DefaultRouter()
router.register('mixtapes',api_views.MixtapeViewSet)
router.register('users',api_views.UserViewSet,basename='users')
router.register('profiles',api_views.ProfileViewSet,basename='profiles')
users_router = routers.NestedSimpleRouter(router,'songs', lookup='song')
users_router.register(
    'songs',
    api_views.MyListView,
    basename='songs',
)

