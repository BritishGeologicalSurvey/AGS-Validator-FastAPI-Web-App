from pydantic import BaseModel, Field
from typing import List


class Validation(BaseModel):
    filename: str = Field(None, example="example.ags")
    filesize: str = Field(None, example="1 kB")
    checker: str = Field(None, example="python_ags4 v0.3.6")
    dictionary: str = Field(None, example="Standard_dictionary_v4_1.ags")
    time: str = Field(None, example="2021-08-18 09:23:29")
    result: str = Field(None, example="All checks passed!")


class Error(BaseModel):
    error: str = Field(..., example="error")
    propName:  str = Field(None, example="error")
    desc: str = Field(..., example="Error message")


class MinimalResponse(BaseModel):
    msg: str = Field(..., example="Example response")
    type: str = Field(..., example="success")
    self: str = Field(..., example="http://example.com/apis/query")


class ErrorResponse(MinimalResponse):
    errors: List[Error] = None


class ValidationResponse(MinimalResponse):
    data: List[Validation] = None
