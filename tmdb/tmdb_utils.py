from typing import List, Dict, Any
from streaming.models import Movie, TVShow


class TMDBUtils:
    @staticmethod
    def get_availables_movies_from_trending(movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        availables_movies = []
        for movie in movies:
            try:
                db_movie = Movie.objects.get(tmdb_id=movie["id"])
                availables_movies.append(db_movie)
            except Movie.DoesNotExist:
                pass

        return availables_movies
    
    @staticmethod
    def get_availables_tvshows_from_trending(tvshows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        available_tvshows = []
        for tvshow in tvshows:
            try:
                tvshow_db = TVShow.objects.get(tmdb_id=tvshow["id"])
                available_tvshows.append(tvshow_db)
            except TVShow.DoesNotExist:
                pass
        
        return available_tvshows
