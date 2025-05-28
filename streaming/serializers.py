from rest_framework import serializers
from .models import *


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "overview", "release_date", "poster"]


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ["id", "episode_number", "name", "overview", "air_date", "thumbnail"]


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ["id", "season_number", "name", "overview", "poster", "air_date", "episodes"]


class TVShowSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = TVShow
        fields = ["id", "tmdb_id", "name", "overview", "first_air_date", "poster", "seasons"]
