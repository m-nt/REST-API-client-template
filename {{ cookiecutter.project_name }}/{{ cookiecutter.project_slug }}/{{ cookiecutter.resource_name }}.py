from typing import Any
from {{ cookiecutter.project_slug }}.handlers.{{ cookiecutter.resource_name }} import Handler
from urllib.parse import urljoin

class {{ cookiecutter.resource_name.capitalize() }}:
    handler: Handler
    api_url: str

    def __init__(self, _handler: Handler, _api_url: str):
        self.api_url = _api_url
        self.handler = _handler

    async def get_{{ cookiecutter.resource_name }}(self, token: str) -> Any:
        return await self.handler._send_request(
            method="GET",
            url=urljoin(self.api_url, "/{{ cookiecutter.resource_name }}"),
            headers={"Authorization": f"Bearer {token}"},
        )
    # TODO: add the rest of the {{ cookiecutter.resource_name }} request methods

