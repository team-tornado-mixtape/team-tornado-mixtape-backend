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
    path('api/my/mixtapes', api_views.UserMixtapeListView.as_view(), name='user_mixtapes'),
    path('api/my/profile', api_views.UserProfileView.as_view(),name='user_profile'),
    path('api/profiles/<int:profile_pk>/followers', api_views.CreateFollowerView.as_view(),name ='create_followers'),
    path('api/mixtapes/<int:mixtape_pk>/favorites', api_views.CreateFavoriteView.as_view(),name ='create_favorites'),
    path('api/my/favorites',api_views.FavoriteMixtapeListView.as_view(),name='list_favorites'),
    path('api/following',api_views.UserFollowingView.as_view(),name='user_following'),
    path('api/followers',api_views.UserFollowersView.as_view(),name='user_followers'),
    path('api/search', api_views.SearchView.as_view(), name='search'),
]
