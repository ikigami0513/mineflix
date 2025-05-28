from django.urls import path
from . import views


urlpatterns = [
    path('movies/search/', views.RetrieveMoviesFromTitleView.as_view(), name='retrieve_movies_from_title_view'),
    path('movies/retrieve/<int:movie_id>/', views.RetrieveMovieFromIDView.as_view(), name='retrive_movie_from_id_view'),
    path('tvshows/search/', views.RetrieveTVShowsFromNameView.as_view(), name='retrieve_tvshows_from_name_view'),
    path('tvshows/retrieve/<int:tvshow_id>/', views.RetrieveTVShowFromIDView.as_view(), name='retrieve_tvshow_from_id_view'),
    path('tvshows/seasons/<uuid:season_id>/episodes/', views.RetrieveEpisodesFromSeason.as_view(), name='retrieve_episodes_season_view')
]
