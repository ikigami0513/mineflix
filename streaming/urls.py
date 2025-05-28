from django.urls import path
from . import views


urlpatterns = [
    path('movies/', views.MovieListView.as_view(), name='movie_list_view'),
    path('movies/<uuid:movie_id>/details/', views.MovieDetailView.as_view(), name='movie_detail_view'),
    path('movies/<uuid:movie_id>/watch/', views.MovieWatchView.as_view(), name='movie_watch_view'),
    path('tvshows/', views.TVShowListView.as_view(), name='tvshow_list_view'),
    path('tvshows/retrieve_by_name/', views.TVShowsRetrieveView.as_view(), name='tvshow_retrieve_by_name'),
    path('tvshows/<uuid:tvshow_id>/details/', views.TVShowDetailView.as_view(), name='tvshow_detail_view'),
    path('tvshows/seasons/<uuid:season_id>/details/', views.SeasonDetailView.as_view(), name='season_detail_view'),
    path('tvshows/episodes/<uuid:episode_id>/watch/', views.EpisodeWatchView.as_view(), name="episode_watch_view")
]
