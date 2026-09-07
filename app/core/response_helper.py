# app/core/response.py

import json
from typing import Any

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class CommonJSONResponse(JSONResponse):
    def __init__(
        self,
        content=None,
        status_code=200,
        message="Request successful",
        success=True,
        **kwargs
    ):
        content = {
            "success": success,
            "message": message,
            "data": jsonable_encoder(content),
        }
        super().__init__(
            content=content,
            status_code=status_code,
            **kwargs)