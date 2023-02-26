import httpx
from httpx import Response, Request
from urllib.parse import urlencode
from typing import Union, Optional, Any

from fastapi import HTTPException

from {{ cookiecutter.project_slug }}.models.{{ cookiecutter.resource_name }} import RequestMethod

HEADERS = {"accept": "application/json", "Content-Type": "application/json"}

message_regex = r"(?<=message[\"']:[\"'])[a-zA-Z0-9 _\-]+|(?<=msg[\"']:[\"'])[a-zA-Z0-9 _\-]+|(?<=message[\"']: [\"'])[a-zA-Z0-9 _\-]+|(?<=msg[\"']: [\"'])[a-zA-Z0-9 _\-]+|(?<=detail[\"']:[\"'])[a-zA-Z0-9 _\-]+|(?<=detail[\"']: [\"'])[a-zA-Z0-9 _\-]+"


class Handler:
    @staticmethod
    def get_response_message_v2(response: Response) -> Any:
        matches = re.findall(message_regex, response.text)
        if len(matches) > 0:
            msg = [msg for msg in matches]
            return {"message": ", ".join(msg[:])}
        else:
            if len(response.text) > 3 and isinstance(response.text, str):
                return {"message": response.text}
            return {"message": "Unknown error"}
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
                status_code=500,
                detail={
                    "message": str(type(error))[8:-2],
                },
            )
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail={
                    "message": Handler.get_response_message_v2(res),
                },
            )
        return res.json()
