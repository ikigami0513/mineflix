from django.contrib import admin
from .models import Movie, TVShow, Season, Episode


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'overview', 'release_date']


@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):
    list_display = ['name', 'overview', 'first_air_date']


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['tv_show', 'name', 'season_number', 'overview', 'air_date']


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'season', 'episode_number', 'overview', 'air_date']
    