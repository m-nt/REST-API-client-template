from pydantic import BaseModel as DefaultModel
from typing import Optional
from enum import Enum


class BaseModel(DefaultModel):
    version: Optional[str] = "{{ cookiecutter.version }}"


class RequestMethod(str, Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"


# TODO: add {{ cookiecutter.resource_name }} models
