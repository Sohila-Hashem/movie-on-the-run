import logging

from abc import ABC, abstractmethod
from app.utils.API_Client import IAPIClient

logger = logging.getLogger(__name__)


class ITrailerAPIService(ABC):
    @abstractmethod
    def __init__(self, client: IAPIClient) -> None:
        pass

    @abstractmethod
    def get_movie_trailers(self, movie_id: int, sites: list[str] = ["YouTube"]) -> list:
        pass


class TrailerAPIService(ITrailerAPIService):
    def __init__(self, client: IAPIClient = None) -> None:
        if not client:
            raise ValueError("client is required")
        self.client: IAPIClient = client

    def get_movie_trailers(self, movie_id: int, sites: list[str] = ["YouTube"]) -> list:
        """
        Fetches the official trailers for a movie.

        Args:
            movie_id (int): The ID of the movie.
            sites (list[str]): Optional. List of sites to filter by.

        Returns:
            list: List of trailers.
        """
        sub_url = f"movie/{movie_id}/videos"

        trailers = self.client.get(sub_url=sub_url)

        if not trailers or not trailers.get("results"):
            return []

        if sites:
            return list(
                filter(
                    lambda video: (
                        video.get("type") == "Trailer"
                        and video.get("site") in sites
                        and video.get("official")
                    ),
                    trailers.get("results"),
                )
            )
        return trailers.get("results")
