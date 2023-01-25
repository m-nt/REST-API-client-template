"""
The MIT License (MIT)

Copyright (c) 2016 Rémy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import httpx
from httpx import Response
from dataclasses import dataclass
from urllib.parse import urljoin
from typing import Union, Optional, Any

from {{ cookiecutter.project_slug }}.models.{{ cookiecutter.resource_name}} import *

HEADERS = {"accept": "application/json", "Content-Type": "application/json"}

class Hander():
    async def __send_post_request(
        self,
        suffixURL: str,
        content: Optional[str] = None,
        headers: Optional[dict] = HEADERS,
    ) -> Union[Any, dict]:
        try:
            async with httpx.AsyncClient(timeout=self.api_timeout) as client:
                res: Response = await client.post(
                    urljoin(self.api_url, suffixURL),
                    content=content,
                    headers=headers,
                )
                client.r
        except httpx.HTTPError as error:
            return models.ErrorResponse(
                fingerprint="",
                errors=[
                    models.Error(**{"code": "500", "message": str(type(error))[8:-2]}),
                ],
            )

        try:
            json_res = res.json()
        except Exception:
            return models.ErrorResponse(
                fingerprint="",
                errors=[
                    models.Error(**{"code": "500", "message": "Invalid response data"})
                ],
            )

        if "errors" in json_res:
            return models.ErrorResponse(**json_res)

        return json_res

    async def __send_get_request(
        self,
        suffixURL: str,
        params: Optional[str] = None,
        headers: Optional[dict] = HEADERS,
    ) -> Union[Any, models.ErrorResponse]:
        try:
            async with httpx.AsyncClient(timeout=self.api_timeout) as client:
                res: Response = await client.get(
                    urljoin(self.api_url, suffixURL),
                    params=params,
                    headers=headers,
                )
        except httpx.HTTPError as error:
            return models.ErrorResponse(
                fingerprint="",
                errors=[
                    models.Error(**{"code": "500", "message": str(type(error))[8:-2]}),
                ],
            )

        if "404 page not found" in res.text:
            return models.ErrorResponse(
                fingerprint="", errors=[models.Error(**{"code": res.text})]
            )

        try:
            json_res = res.json()
        except Exception:
            return models.ErrorResponse(
                fingerprint="",
                errors=[
                    models.Error(**{"code": "500", "message": "Invalid response data"})
                ],
            )

        if "errors" in json_res:
            return models.ErrorResponse(**json_res)

        return json_res