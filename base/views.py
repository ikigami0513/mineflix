from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from streaming.models import Movie, Season


class IndexView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> HttpResponse:
        last_movies = Movie.objects.order_by('-added_at')[:6]
        seasons = Season.objects.select_related('tv_show').order_by('-added_at')
        last_seasons = []
        tvshow_names = set()
        for season in seasons:
            if season.tv_show.name not in tvshow_names:
                last_seasons.append(season)
                tvshow_names.add(season.tv_show.name)
                if len(last_seasons) >= 6:
                    break

        return render(request, "index.html", {
            "last_movies": last_movies,
            "last_season": last_seasons
        })
    