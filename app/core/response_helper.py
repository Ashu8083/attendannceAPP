# app/core/response.py

import json
from typing import Any

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class CommonJSONResponse(JSONResponse):

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        message: str = "Request successful",
        success: bool = True,
        headers=None,
        media_type=None,
        background=None,
    ):
        content = {
            "success": success,
            "message": message,
            "data": jsonable_encoder(content)
        }

        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background
        )