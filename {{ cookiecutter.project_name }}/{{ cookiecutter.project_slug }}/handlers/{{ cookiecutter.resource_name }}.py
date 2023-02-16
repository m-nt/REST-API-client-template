import httpx
from httpx import Response, Request
from urllib.parse import urlencode
from typing import Union, Optional, Any

from fastapi import HTTPException

from {{ cookiecutter.project_slug }}.models.{{ cookiecutter.resource_name }} import RequestMethod

HEADERS = {"accept": "application/json", "Content-Type": "application/json"}


class Handler:
    @staticmethod
    def get_response_message(response: Response) -> Any:
        try:
            data = response.json()
        except Exception as e:
            return {"message": "Unknown error"}
        if "detail" in data:
            return data["detail"]
        if "content" in data:
            return data["content"]
        if "message" in data:
            return data
        
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
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                res: Response = await client.send(_request)
        except Exception as error:
            raise HTTPException(
                status_code=res.status_code,
                detail={
                    "message": str(type(error))[8:-2],
                },
            )
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail={
                    "message": Handler.get_response_message(res),
                },
            )
        return res.json()
