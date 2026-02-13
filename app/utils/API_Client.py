from abc import ABC, abstractmethod
from requests_toolbelt import sessions


class IAPIClient(ABC):
    @abstractmethod
    def __init__(self, base_url: str, params: object, headers: object) -> None:
        pass

    @abstractmethod
    def get(self, sub_url: str, params: object = None) -> object:
        pass


class APIClient(IAPIClient):
    def __init__(self, base_url: str, params: object, headers: object) -> None:
        self.client = sessions.BaseUrlSession(base_url)
        self.client.headers = headers
        self.default_params = params

    def get(self, sub_url: str, params: object = None) -> object:
        """
        Make a GET request to the API.

        Args:
            sub_url (str): The sub URL.
            params (object, optional): The parameters. Defaults to None.

        Returns:
            object: The response from the API.
        """
        final_params = self.default_params.copy() if self.default_params else {}
        if params:
            final_params.update(params)
        return self.client.get(url=sub_url, params=final_params).json()
