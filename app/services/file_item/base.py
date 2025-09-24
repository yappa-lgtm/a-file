import os
import re
import urllib.parse
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from core.exceptions import (
    PathException,
    FileItemNotFoundException,
    FileNotFoundException,
)
from core.models import FileItem
from core.schemas.file_item import FileItemRead, FileItemRename
from utils.path import create_safe_file_path

UPLOAD_PATH = Path.cwd().parent / "uploads"


class FileItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

        UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

    async def create(
        self, file: UploadFile, path: str, filename: Optional[str]
    ) -> FileItemRead:
        if not re.match(r"^/([A-Za-z0-9._-]+/?)*$", path):
            raise PathException(path=path, reason="Неправильний формат шляху")

        file_item = FileItem(
            filename=filename,
            original_filename=file.filename,
            file_path=path,
            file_size=file.size,
            mime_type=file.content_type or "application/octet-stream",
            file_extension=Path(file.filename).suffix.lstrip("."),
        )

        self.session.add(file_item)
        await self.session.commit()

        filename_with_id = f"{file_item.id}.{file_item.file_extension}"
        file_path = create_safe_file_path(UPLOAD_PATH, path, filename_with_id)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return FileItemRead.model_validate(file_item, from_attributes=True)

    async def find_by_id(self, file_id: str) -> FileItemRead:
        stmt = select(FileItem).where(FileItem.id == file_id)
        result = await self.session.execute(stmt)
        file_item: FileItem = result.scalar_one_or_none()

        if file_item is None:
            raise FileItemNotFoundException(file_id=file_id)

        return FileItemRead.model_validate(file_item, from_attributes=True)

    async def download_by_id(self, file_id: str) -> FileResponse:
        stmt = select(FileItem).where(FileItem.id == file_id)
        result = await self.session.execute(stmt)
        file_item: FileItem = result.scalar_one_or_none()

        if file_item is None:
            raise FileItemNotFoundException(file_id=file_id)

        filename_with_id = f"{file_item.id}.{file_item.file_extension}"
        file_path = create_safe_file_path(
            UPLOAD_PATH, file_item.file_path, filename_with_id
        )

        if not file_path.exists():
            raise FileNotFoundException(
                file_path=f"{file_item.file_path}/{filename_with_id}"
            )

        filename = file_item.filename or file_item.original_filename

        encoded_filename = urllib.parse.quote(filename.encode("utf-8"))

        return FileResponse(
            path=str(file_path),
            media_type=file_item.mime_type,
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            },
        )

    async def rename(self, dto: FileItemRename) -> FileItemRead:
        stmt = select(FileItem).where(FileItem.id == dto.id)
        result = await self.session.execute(stmt)
        file_item: FileItem = result.scalar_one_or_none()

        if file_item is None:
            raise FileItemNotFoundException(file_id=dto.id)

        file_item.filename = f"{dto.new_filename}.{file_item.file_extension}"

        await self.session.commit()
        await self.session.refresh(file_item)

        return FileItemRead.model_validate(file_item, from_attributes=True)

    async def delete_by_id(self, file_id: str) -> FileItemRead:
        stmt = select(FileItem).where(FileItem.id == file_id)
        result = await self.session.execute(stmt)
        file_item: FileItem = result.scalar_one_or_none()

        if file_item is None:
            raise FileItemNotFoundException(file_id=file_id)

        filename_with_id = f"{file_item.id}.{file_item.file_extension}"
        file_path = create_safe_file_path(
            UPLOAD_PATH, file_item.file_path, filename_with_id
        )

        if file_path.exists():
            os.remove(file_path)

        await self.session.delete(file_item)
        await self.session.commit()

        return FileItemRead.model_validate(file_item, from_attributes=True)
