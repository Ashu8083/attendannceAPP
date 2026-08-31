from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class CommonResponse(BaseModel,Generic[T]):
    success: bool = True
    message: str = "Request successful"
    data: T | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total: int
    total_pages: int