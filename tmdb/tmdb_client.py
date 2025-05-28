from tmdbv3api import TMDb, Movie, TV, Season, Trending
from typing import List, Optional, Dict, Any


class TMDBClient:
    def __init__(self, api_key: str, language: str = 'fr', debug: bool = False) -> None:
        self.tmdb = TMDb()
        self.tmdb.api_key = api_key
        self.tmdb.language = language
        self.tmdb.debug = debug

        self.movie_api = Movie()
        self.tv_api = TV()
        self.season_api = Season()
        self.trending_api = Trending()

    def search_movies(self, query: str) -> List[Dict[str, Any]]:
        results = self.movie_api.search(query)
        return [self._format_movie_result(m) for m in results]
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict[str, Any]]:
        try:
            movie = self.movie_api.details(movie_id)
            return self._format_movie_result(movie)
        except Exception:
            return None
        
    def get_movie_images(self, movie_id: int) -> Optional[Dict[str, List[str]]]:
        try:
            images = self.movie_api.images(movie_id)
            base_url = "https://image.tmdb.org/t/p/"
            return {
                "posters": [f"{base_url}w342{img['file_path']}" for img in images.get("posters", [])],
                "backdrops": [f"{base_url}w780{img['file_path']}" for img in images.get("backdrops", [])]
            }
        except Exception:
            return None
        
    def get_trending_movies(self, time_window: str = "day") -> List[Dict[str, Any]]:
        try:
            results = getattr(self.trending_api, f"movie_{time_window}")()
            return [self._format_movie_result(movie) for movie in results['results']]
        except Exception as e:
            print(f"Error fetching trending movies: {e}")
            return []
        
    def get_trending_tvshows(self, time_window: str = "day"):
        try:
            results = getattr(self.trending_api, f"tv_{time_window}")()
            return [self._format_tv_result(tvshow) for tvshow in results['results']]
        except Exception as e:
            print(f"Error fetching trending tvshows: {e}")
            return []
        
    def search_tv_shows(self, query: str) -> List[Dict[str, Any]]:
        results = self.tv_api.search(query)
        return [self._format_tv_result(tv) for tv in results]
    
    def get_tv_show_details(self, tv_id: int) -> Optional[Dict[str, Any]]:
        try:
            tv_show = self.tv_api.details(tv_id)
            return self._format_tv_result(tv_show)
        except Exception:
            return None
        
    def get_season_episodes(self, tv_id: int, season_number: int) -> Optional[List[Dict[str, Any]]]:
        try:
            season = self.season_api.details(tv_id, season_number)
            return [self._format_episode_result(episode) for episode in getattr(season, "episodes", [])]
        except Exception as e:
            print(f"Error fetching season episodes: {e}")
            return None
        
    def _format_movie_result(self, movie: Any) -> Dict[str, Any]:
        return {
            "id": movie.id,
            "title": getattr(movie, "title", ""),
            "overview": getattr(movie, "overview", ""),
            "release_date": getattr(movie, "release_date", ""),
            "poster_path": getattr(movie, "poster_path", ""),
            "vote_average": getattr(movie, "vote_average", 0.0),
        }
    
    def _format_season_result(self, season: Any) -> Dict[str, Any]:
        return {
            "season_number": season.season_number,
            "episode_count": getattr(season, "episode_count", None),
            "air_date": getattr(season, "air_date", ""),
            "name": getattr(season, "name", ""),
            "overview": getattr(season, "overview", ""),
            "poster_path": getattr(season, "poster_path", "")
        }
    
    def _format_episode_result(self, episode: Any) -> Dict[str, Any]:
        return {
            "id": episode.id,
            "episode_number": getattr(episode, "episode_number", None),
            "name": getattr(episode, "name", ""),
            "overview": getattr(episode, "overview", ""),
            "air_date": getattr(episode, "air_date", ""),
            "still_path": getattr(episode, "still_path", ""),
            "vote_average": getattr(episode, "vote_average", 0.0),
            "vote_count": getattr(episode, "vote_count", 0)
        }
    
    def _format_tv_result(self, tv: Any) -> Dict[str, Any]:
        return {
            "id": tv.id,
            "name": getattr(tv, "name", ""),
            "overview": getattr(tv, "overview", ""),
            "first_air_date": getattr(tv, "first_air_date", ""),
            "poster_path": getattr(tv, "poster_path", ""),
            "vote_average": getattr(tv, "vote_average", 0.0),
            "seasons": [self._format_season_result(season) for season in getattr(tv, "seasons", [])]
        }
    