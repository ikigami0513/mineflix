from django.urls import path
from . import views


urlpatterns = [
    path('', views.DashboardIndexView.as_view(), name='dashboard_index'),
    path('movies/add/', views.AddMovieFromDashboardView.as_view(), name='add_movie_dashboard_view'),
    path('tvshows/add/', views.AddTVShowFromDashboardView.as_view(), name='add_tvshow_dashboard_view'),
    path('tvshows/seasons/add/', views.AddSeasonFromDashboardView.as_view(), name='add_season_dashboard_view'),
    path('tvshows/episodes/add/', views.AddEpisodeFromDashboardView.as_view(), name='add_episode_dashboard_view')
]
