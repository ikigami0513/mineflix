import os
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import superuser_required
from streaming.models import Movie, TVShow, Season, Episode


class DashboardIndexView(View):
    @method_decorator([login_required, superuser_required])
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "dashboard/index.html")
    

class AddMovieFromDashboardView(View):
    @method_decorator([login_required, superuser_required])
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "dashboard/add_movie.html")
    
    @method_decorator([login_required, superuser_required])
    def post(self, request: HttpRequest) -> HttpResponse:
        data = request.POST
        movie = Movie()
        movie.tmdb_id = data.get("tmdbID")
        movie.title = data.get("movieName")
        movie.overview = data.get("movieOverview")
        movie.release_date = data.get("movieReleaseDate")

        movie_poster_path = data.get("moviePosterPath")
        if movie_poster_path:
            response = requests.get(movie_poster_path)
            if response.status_code != 200:
                raise ValueError(f"Unable to download poster: status {response.status_code}")
            
            parsed_url = urlparse(movie_poster_path)
            filename = os.path.basename(parsed_url.path)

            image_file = ContentFile(response.content)
            movie.poster.save(filename, image_file, save=True)

        movie_thumbnail_path = data.get("movieSelectedThumbnail")
        if movie_thumbnail_path:
            response = requests.get(movie_thumbnail_path)
            if response.status_code != 200:
                raise ValueError(f"Unable to download thumbnail: status {response.status_code}")
            
            parsed_url = urlparse(movie_thumbnail_path)
            filename = os.path.basename(parsed_url.path)

            image_file = ContentFile(response.content)
            movie.thumbnail.save(filename, image_file, save=True)

        video_file = request.FILES.get('movieVideo')
        if video_file:
            movie.video = video_file

        movie.save()

        return redirect("add_movie_dashboard_view")
    

class AddTVShowFromDashboardView(View):
    @method_decorator([login_required, superuser_required])
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "dashboard/add_tvshow.html")
    
    @method_decorator([login_required, superuser_required])
    def post(self, request: HttpRequest) -> HttpResponse:
        data = request.POST
        tvshow = TVShow()
        tvshow.tmdb_id = data.get("tmdbID")
        tvshow.name = data.get("tvshowName")
        tvshow.overview = data.get("tvshowOverview")
        tvshow.first_air_date = data.get("tvshowReleaseDate")

        tvshow_poster_path = data.get("tvshowPosterPath")
        if tvshow_poster_path:
            response = requests.get(tvshow_poster_path)
            if response.status_code != 200:
                raise ValueError(f"Unable to download poster: status {response.status_code}")
            
            parsed_url = urlparse(tvshow_poster_path)
            filename = os.path.basename(parsed_url.path)

            image_file = ContentFile(response.content)
            tvshow.poster.save(filename, image_file, save=True)

        tvshow.save()
        return redirect("add_tvshow_dashboard_view")
    

class AddSeasonFromDashboardView(View):
    @method_decorator([login_required, superuser_required])
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "dashboard/add_season.html")
    
    @method_decorator([login_required, superuser_required])
    def post(self, request: HttpRequest) -> HttpResponse:
        data = request.POST
        tvshow_id = data.get("tvshowID")
        tvshow = TVShow.objects.get(id=tvshow_id)
        season = Season()
        season.tv_show = tvshow
        season.season_number = data.get("seasonNumber")

        if data.get("seasonNameForm") != f"Saison {season.season_number}":
            season.name = data.get("seasonNameForm")

        season.overview = data.get("seasonOverview")
        if season.overview == "" or season.overview is None:
            season.overview = tvshow.overview
            
        season.air_date = data.get("seasonReleaseDate")
        
        season_poster_path = data.get("seasonPosterPath")
        if season_poster_path:
            response = requests.get(season_poster_path)
            if response.status_code != 200:
                raise ValueError(f"Unable to download poster: status {response.status_code}")
            
            parsed_url = urlparse(season_poster_path)
            filename = os.path.basename(parsed_url.path)

            image_file = ContentFile(response.content)
            season.poster.save(filename, image_file, save=True)

        season.save()
        return redirect("add_season_dashboard_view")


class AddEpisodeFromDashboardView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "dashboard/add_episode.html")
    
    def post(self, request: HttpRequest) -> HttpResponse:
        data = request.POST

        tvshow = TVShow.objects.get(id=data.get("tvshowID"))
        season = Season.objects.get(tv_show=tvshow, season_number=data.get("seasonNumber"))
        episode = Episode()
        episode.season = season
        episode.episode_number = data.get("episodeNumber")
        episode.name = data.get("episodeNameForm")
        episode.overview = data.get("episodeOverview")
        episode.air_date = data.get("episodeReleaseDate")

        thumbnail_path = data.get("episodeThumbnailPath")
        if thumbnail_path:
            response = requests.get(thumbnail_path)
            if response.status_code != 200:
                raise ValueError(f"Unable to download poster: status {response.status_code}")
            
            parsed_url = urlparse(thumbnail_path)
            filename = os.path.basename(parsed_url.path)

            image_file = ContentFile(response.content)
            episode.thumbnail.save(filename, image_file, save=True)

        video_file = request.FILES.get('episodeVideo')
        if video_file:
            episode.video = video_file

        episode.save()

        return redirect("add_episode_dashboard_view")
