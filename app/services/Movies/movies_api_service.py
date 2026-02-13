import random
from app.utils.API_Client import IAPIClient
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class IMovieAPIService(ABC):
    @abstractmethod
    def __init__(self, movies_api_client: IAPIClient) -> None:
        pass

    @abstractmethod
    def fetch_movies(self, category_id: int, page: int = 1) -> object:
        pass

    @abstractmethod
    def get_random_movie(self, category_id: int) -> list:
        pass


class MovieAPIService(IMovieAPIService):
    def __init__(self, movies_api_client: IAPIClient) -> None:
        if not movies_api_client:
            raise ValueError("movies_api_client is required")
        self.movies_api_client: IAPIClient = movies_api_client

    def fetch_movies(self, category_id: int, page: int = 1) -> object:
        """
        Fetches the movies for a category.

        Args:
            category_id (int): The ID of the category.
            page (int): The page number.

        Returns:
            object: Response from the API.
        """
        sub_url = "discover/movie"
        params = {
            "page": page,
            "with_genres": category_id,
        }

        data = self.movies_api_client.get(sub_url=sub_url, params=params)
        return data

    def get_random_movie(self, category_id: int) -> list:
        MAX_PAGE = 500
        """
        Gets a random movie for a category.

        Args:
            category_id (int): The ID of the category.

        Returns:
            list: The random movie.
        """
        movies_list = self.fetch_movies(category_id=category_id)
        total_pages = movies_list.get("total_pages")
        random_page = random.randint(1, min(total_pages, MAX_PAGE))
        random_movie_list = self.fetch_movies(category_id=category_id, page=random_page)
        random_movie = random.choice(seq=random_movie_list.get("results"))

        if not random_movie:
            raise ValueError("No movies found")
        return random_movie
