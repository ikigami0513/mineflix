import uuid
from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *


class MovieDetailView(APIView):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, movie_id: uuid.UUID) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MovieListView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> HttpResponse:
        query = request.GET.get("query")
        if query:
            movies = Movie.objects.filter(title__icontains=query)
        else:
            movies = Movie.objects.all().order_by('title')

        paginator = Paginator(movies, 18)
        page = request.GET.get('page')

        try:
            movies_page = paginator.page(page)
        except PageNotAnInteger:
            movies_page = paginator.page(1)
        except EmptyPage:
            movies_page = paginator.page(paginator.num_pages)

        return render(request, "streaming/movie/list.html", {
            "movies": movies_page,
            "query": query
        })
    

class MovieWatchView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, movie_id: uuid.UUID) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        return render(request, "streaming/movie/movie.html", context={
            "movie": movie
        })
    

class TVShowsRetrieveView(APIView):
    @method_decorator(login_required)
    def get(self, request: HttpRequest):
        query = request.GET.get("q")
        if not query:
            return Response({"detail": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        tvshows = TVShow.objects.filter(name__icontains=query).order_by("name")
        serializer = TVShowSerializer(tvshows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TVShowDetailView(APIView):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, tvshow_id: uuid.UUID) -> Response:
        tvshow = get_object_or_404(TVShow, id=tvshow_id)
        serializer = TVShowSerializer(tvshow)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SeasonDetailView(APIView):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, season_id: uuid.UUID) -> Response:
        season = get_object_or_404(Season, id=season_id)
        serializer = SeasonSerializer(season)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TVShowListView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> HttpResponse:
        query = request.GET.get("query")
        if query:
            tvshows = TVShow.objects.filter(name__icontains=query)
        else:
            tvshows = TVShow.objects.all().order_by('name')

        paginator = Paginator(tvshows, 18)
        page = request.GET.get('page')

        try:
            tvshows_page = paginator.page(page)
        except PageNotAnInteger:
            tvshows_page = paginator.page(1)
        except EmptyPage:
            tvshows_page = paginator.page(paginator.num_pages)

        return render(request, "streaming/tvshow/list.html", {
            "tvshows": tvshows_page,
            "query": query
        })
    

class EpisodeWatchView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, episode_id: uuid.UUID) -> HttpResponse:
        episode = get_object_or_404(Episode, id=episode_id)
        try:
            next_episode = Episode.objects.get(season=episode.season, episode_number=episode.episode_number + 1)
        except Episode.DoesNotExist:
            next_episode = None
            
        return render(request, "streaming/tvshow/episode.html", context={
            "episode": episode,
            "next_episode": next_episode
        })
