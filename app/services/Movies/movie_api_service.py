from app.utils.API_Client import IAPIClient
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class IMovieAPIService(ABC):
    @abstractmethod
    def __init__(self, client: IAPIClient) -> None:
        pass

    @abstractmethod
    def get_movies(self, categoryId: int, page: int = 1) -> list:
        pass


class MovieAPIService(IMovieAPIService):
    def __init__(self, client: IAPIClient) -> None:
        if not client:
            raise ValueError("client is required")
        self.client: IAPIClient = client

    def get_movies(self, categoryId: int, page: int = 1) -> list:
        url = "discover/movie"

        params = {
            "page": page,
            "with_genres": categoryId,
        }

        try:
            data = self.client.get(url, params)
            return data
        except Exception as e:
            logger.exception("something went wrong while fetching movies: %s", e)
            return None


class MovieAPIServiceManager:
    _instance = None

    @staticmethod
    def get_instance(client: IAPIClient = None) -> IMovieAPIService:
        if MovieAPIServiceManager._instance is None:
            if client is None:
                raise ValueError(
                    "Client must be provided during the first instantiation."
                )
            MovieAPIServiceManager._instance: IMovieAPIService = MovieAPIService(client)
        return MovieAPIServiceManager._instance
