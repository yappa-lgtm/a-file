from datetime import datetime
from typing import Optional

from pydantic import UUID4

from .base import BaseSchema


class FileItem(BaseSchema):
    filename: Optional[str] = None
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    file_extension: str
    created_at: datetime
    updated_at: datetime


class FileItemRead(FileItem):
    id: UUID4


class FileItemRename(BaseSchema):
    id: UUID4
    new_filename: str

