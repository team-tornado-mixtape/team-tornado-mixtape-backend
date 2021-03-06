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
    path('__debug__/', include('debug_toolbar.urls')),

    path('api/', include(router.urls)),
    path('api/my/mixtapes', api_views.UserMixtapeListView.as_view(), name='user_mixtapes'),
    path('api/my/mixtapes/', api_views.UserMixtapeListView.as_view(), name='user_mixtapes'),
    path('api/my/profile', api_views.UserProfileView.as_view(),name='user_profile'),
    path('api/my/profile/', api_views.UserProfileView.as_view(),name='user_profile'),
    path('api/profiles/<int:profile_pk>/following', api_views.CreateUpdateFollowingView.as_view(),name ='create_following'),
    path('api/profiles/<int:profile_pk>/following/', api_views.CreateUpdateFollowingView.as_view(),name ='create_following'),
    path('api/mixtapes/<int:mixtape_pk>/favorites', api_views.CreateUpdateFavoriteView.as_view(),name ='create_favorites'),
    path('api/mixtapes/<int:mixtape_pk>/favorites/', api_views.CreateUpdateFavoriteView.as_view(),name ='create_favorites'),
    path('api/my/favorites',api_views.FavoriteMixtapeListView.as_view(),name='list_favorites'),
    path('api/my/favorites/',api_views.FavoriteMixtapeListView.as_view(),name='list_favorites'),
    path('api/following',api_views.UserFollowingView.as_view(),name='user_following'),
    path('api/following/',api_views.UserFollowingView.as_view(),name='user_following'),
    path('api/followers',api_views.UserFollowersView.as_view(),name='user_followers'),
    path('api/followers/',api_views.UserFollowersView.as_view(),name='user_followers'),
    path('api/search', api_views.SearchView.as_view(), name='search'),
    path('api/my/profile/<int:profile_pk>/image/',api_views.ImageUploadView.as_view(
        {'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
        }
    ), name = 'update_profile_pic'),
    path('api/mixtapes/<int:mixtape_pk>/songs/<int:song_pk>', api_views.MixtapeUpdateView.as_view(), name ='update_mixtape_songs'),
    path('api/mixtapes/<int:mixtape_pk>/songs/<int:song_pk>', api_views.MixtapeUpdateView.as_view(), name ='update_mixtape_songs'),

    path('api/mixtapes/<int:mixtape_pk>/spotify', api_views.TransferSpotifyMixtape.as_view(),name='to_spotify'),
    path('api/mixtapes/<int:mixtape_pk>/spotify/', api_views.TransferSpotifyMixtape.as_view(),name='to_spotify'),
    path('api/mixtapes/<int:mixtape_pk>/apple', api_views.TransferAppleMixtape.as_view(),name='to_apple'),
    path('api/mixtapes/<int:mixtape_pk>/apple/', api_views.TransferAppleMixtape.as_view(),name='to_apple'),
]
