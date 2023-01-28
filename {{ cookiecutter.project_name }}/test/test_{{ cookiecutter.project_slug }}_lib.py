from {{ cookiecutter.project_slug }} import __version__
import pytest
from typing import Any
from fastapi import HTTPException

from {{ cookiecutter.project_slug }}.{{ cookiecutter.resource_name }} import {{ cookiecutter.resource_name.capitalize() }}
from {{ cookiecutter.project_slug }}.handlers.{{ cookiecutter.resource_name }} import Handler

{{ cookiecutter.resource_name }}_hander = {{ cookiecutter.resource_name.capitalize() }}(Handler, "http://localhost:8000/")

token = "token"

def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.asyncio()
async def test_api_{{ cookiecutter.resource_name }}_error():
    with pytest.raises(HTTPException) as exc_info:
        await {{ cookiecutter.resource_name }}_hander.get_{{ cookiecutter.resource_name }}(token="test")
    assert exc_info.value.status_code == 511


@pytest.mark.asyncio()
async def test_api_{{ cookiecutter.resource_name }}_no_error():
    res = await {{ cookiecutter.resource_name }}_hander.get_{{ cookiecutter.resource_name }}(token=token)
    assert type(res) is dict