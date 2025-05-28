from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from streaming.models import Movie, Season
from authentication.models import User
from tmdb.tmdb_client import TMDBClient
from tmdb.tmdb_utils import TMDBUtils
from typing import List


class IndexView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> HttpResponse:
        last_movies = Movie.objects.order_by('-added_at')[:6]
        last_seasons = self.get_last_seasons()

        user = User.objects.get(username="admin")
        client = TMDBClient(api_key=user.tmdb_api_key)
        trending_movies = TMDBUtils.get_availables_movies_from_trending(client.get_trending_movies())
        trending_tvshows = TMDBUtils.get_availables_tvshows_from_trending(client.get_trending_tvshows())

        return render(request, "index.html", {
            "last_movies": last_movies,
            "last_season": last_seasons,
            "trending_movies": trending_movies,
            "trending_tvshows": trending_tvshows
        })
    
    def get_last_seasons(self) -> List[Season]:
        seasons = Season.objects.select_related('tv_show').order_by('-added_at')
        last_seasons = []
        tvshow_names = set()
        for season in seasons:
            if season.tv_show.name not in tvshow_names:
                last_seasons.append(season)
                tvshow_names.add(season.tv_show.name)
                if len(last_seasons) >= 6:
                    break
        return last_seasons
    