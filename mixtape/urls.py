"""mixtape URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from api.router import router
from api import views as api_views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),

    path('api/', include(router.urls)),
    path('api/users/<int:pk>/mixtapes', api_views.UserMixtapeListView.as_view(), name='user_mixtapes'),
    path('api/users/<int:pk>/profile', api_views.UserProfileView.as_view(),name='user_profile'),
    path('api/profiles/<int:profile_pk>/followers', api_views.CreateFollowerView.as_view(), name ='create_followers'),

]
 