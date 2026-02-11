import logging

from abc import ABC, abstractmethod
from app.utils.API_Client import IAPIClient

logger = logging.getLogger(__name__)


class ITrailerAPIService(ABC):
    @abstractmethod
    def __init__(self, client: IAPIClient) -> None:
        pass

    @abstractmethod
    def get_movie_trailers(self, movie_id: int) -> list:
        pass


class TrailerAPIService(ITrailerAPIService):
    def __init__(self, client: IAPIClient = None) -> None:
        if not client:
            raise ValueError("client is required")
        self.client: IAPIClient = client

    def get_movie_trailers(self, movie_id: int) -> list:
        url = f"movie/{movie_id}/videos"

        try:
            data = self.client.get(url)

            if data and len(data["results"]):
                return data["results"]
            return None
        except Exception as e:
            logger.exception("something went wrong while getting movie trailers: %s", e)
            return None


class TrailerAPIServiceManager:
    _instance = None

    @staticmethod
    def get_instance(client: IAPIClient = None) -> TrailerAPIService:
        if TrailerAPIServiceManager._instance is None:
            if client is None:
                raise ValueError(
                    "Client must be provided during the first instantiation."
                )
            TrailerAPIServiceManager._instance: ITrailerAPIService = TrailerAPIService(
                client
            )
        return TrailerAPIServiceManager._instance
