import uuid
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .tmdb_client import TMDBClient
from dashboard.decorators import superuser_required
from authentication.models import User
from streaming.models import Season


class RetrieveMoviesFromTitleView(APIView):
    @method_decorator([login_required, superuser_required])
    def get(self, request: HttpRequest) -> Response:
        query = request.GET.get("q")
        if not query:
            return Response(
                {"detail": "Le paramètre 'q' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user: User = request.user
        client = TMDBClient(user.tmdb_api_key)
        movies = client.search_movies(query)
        return Response(movies, status=status.HTTP_200_OK)
    

class RetrieveMovieFromIDView(APIView):
    @method_decorator([login_required, superuser_required])
    def get(self, request: HttpRequest, movie_id: int) -> Response:
        user: User = request.user
        client = TMDBClient(user.tmdb_api_key)
        movie = client.get_movie_details(movie_id)
        movie.update(client.get_movie_images(movie_id))
        return Response(movie, status=status.HTTP_200_OK)


class RetrieveTVShowsFromNameView(APIView):
    @method_decorator([login_required, superuser_required])
    def get(self, request: HttpRequest) -> Response:
        query = request.GET.get("q")
        if not query:
            return Response(
                {"detail": "Le paramètre 'q' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user: User = request.user
        client = TMDBClient(user.tmdb_api_key)
        tvshows = client.search_tv_shows(query)
        return Response(tvshows, status=status.HTTP_200_OK)


class RetrieveTVShowFromIDView(APIView):
    @method_decorator([login_required, superuser_required])
    def get(self, request: HttpRequest, tvshow_id: int) -> Response:
        user: User = request.user
        client = TMDBClient(user.tmdb_api_key)
        tvshow = client.get_tv_show_details(tvshow_id)
        return Response(tvshow, status=status.HTTP_200_OK)


class RetrieveEpisodesFromSeason(APIView):
    @method_decorator([login_required, superuser_required])
    def get(self, request: HttpRequest, season_id: uuid.UUID) -> Response:
        user: User = request.user
        client = TMDBClient(user.tmdb_api_key)
        season = Season.objects.get(id=season_id)
        episodes = client.get_season_episodes(season.tv_show.tmdb_id, season.season_number)
        return Response(episodes, status=status.HTTP_200_OK)
