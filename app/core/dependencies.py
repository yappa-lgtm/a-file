from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from services.file_item import FileItemService


def get_file_item_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> FileItemService:
    return FileItemService(session=session)
