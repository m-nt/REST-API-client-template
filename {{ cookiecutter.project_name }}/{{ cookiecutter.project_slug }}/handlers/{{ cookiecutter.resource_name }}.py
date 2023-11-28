import httpx
from httpx import Response, Request
from urllib.parse import urlencode
from typing import Union, Optional, Any

from fastapi import HTTPException

from {{ cookiecutter.project_slug }}.models.{{ cookiecutter.resource_name }} import RequestMethod

HEADERS = {"accept": "application/json", "Content-Type": "application/json"}

class Handler:
    @staticmethod
    async def _send_request(
        method: RequestMethod,
        url: str,
        parameters: Optional[dict] = None,
        content: Optional[str] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = 5,
    ) -> Union[Any, dict]:
        if parameters:
            _params = urlencode(
                parameters,
            )
        else:
            _params = None
        if not headers:
            _headers = HEADERS
        else:
            _headers = {**headers, **HEADERS}

        _request = Request(
            method=method,
            url=url,
            params=_params,
            content=content,
            json=json,
            headers=_headers,
        )
        async with httpx.AsyncClient(timeout=timeout) as client:
            res: Response = await client.send(_request)
            if res.status_code != 200:
                raise HTTPException(
                    status_code=res.status_code,
                    detail=res.json(),
                )
            return res.json()
