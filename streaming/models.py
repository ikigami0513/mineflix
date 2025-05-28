import os
import uuid
from django.db import models
from moviepy import VideoFileClip
from datetime import timedelta, datetime


def movie_poster_file_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return os.path.join(f"streaming/movie/posters/{instance.id}.{uuid.uuid4()}{file_extension}")


def movie_thumbnail_file_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return os.path.join(f"streaming/movie/thumbnail/{instance.id}.{uuid.uuid4()}{file_extension}")


def tv_show_poster_file_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return os.path.join(f"streaming/tv_shows/posters/tv_shows/{instance.id}.{uuid.uuid4()}{file_extension}")


def season_poster_file_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return os.path.join(f"streaming/tv_shows/posters/seasons/{instance.id}.{uuid.uuid4()}{file_extension}")

def episode_thumbnail_file_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return os.path.join(f"streaming/tv_shows/thumbnails/episodes/{instance.id}.{uuid.uuid4()}{file_extension}")



def movie_video_file_path(instance: 'Movie', filename):
    _, file_extension = os.path.splitext(filename)
    return os.path.join(f"streaming/movie/videos/{uuid.uuid4()}{file_extension}")


def episode_video_file_path(instance: 'Episode', filename):
    _, file_extension = os.path.splitext(filename)
    return os.path.join(f"streaming/tv_shows/episodes/{uuid.uuid4()}{file_extension}")


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tmdb_id = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    poster = models.ImageField(upload_to=movie_poster_file_path, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=movie_thumbnail_file_path, null=True, blank=True)
    video = models.FileField(upload_to=movie_video_file_path)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    

class TVShow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tmdb_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    first_air_date = models.DateField(blank=True, null=True)
    poster = models.ImageField(upload_to=tv_show_poster_file_path, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    

class Season(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.PositiveIntegerField()
    name = models.CharField(max_length=255, null=True, blank=True)
    overview = models.TextField(blank=True, null=True)
    poster = models.ImageField(upload_to=season_poster_file_path, null=True, blank=True)
    air_date = models.DateField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tv_show', 'season_number')
        ordering = ['tv_show__name', 'season_number']

    def __str__(self) -> str:
        return f"Saison {self.season_number} - {self.tv_show.name}"
    

def get_video_duration(file_path: str) -> timedelta:
    with VideoFileClip(file_path) as clip:
        return timedelta(seconds=clip.duration)
    

class Episode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    air_date = models.DateField(blank=True, null=True)
    video = models.FileField(upload_to=episode_video_file_path)
    thumbnail = models.ImageField(upload_to=episode_thumbnail_file_path, null=True, blank=True)
    credits_time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('season', 'episode_number')
        ordering = ['season__tv_show__name', 'season__season_number', 'episode_number']

    def save(self, *args, **kwargs) -> None:
        if self.video and not self.credits_time:
            video_path = self.video.path
            if os.path.exists(video_path):
                duration = get_video_duration(video_path)
                credits_start = (datetime.min + duration - timedelta(minutes=1)).time()
                self.credits_time = credits_start

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Épisode {self.episode_number} - {self.name}"
    