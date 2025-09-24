import logging

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import UUID4

from core.dependencies import get_file_item_service
from core.exceptions import ApplicationException
from core.schemas.file_item import FileItemRead, FileItemRename
from services.file_item import FileItemService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["File Items"])


@router.post("/", response_model=FileItemRead)
async def create(
    file: UploadFile = File(...),
    path: str = Form(...),
    service: FileItemService = Depends(get_file_item_service),
):
    try:
        result = await service.create(file=file, path=path)
        return result
    except ApplicationException as e:
        return e.to_json_response()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return ApplicationException().to_json_response()


@router.get("/{file_id}", response_model=FileItemRead)
async def find_by_id(
    file_id: UUID4, service: FileItemService = Depends(get_file_item_service)
):
    try:
        result = await service.find_by_id(file_id=file_id)
        return result
    except ApplicationException as e:
        return e.to_json_response()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return ApplicationException().to_json_response()


@router.get("/download/{file_id}", response_class=FileResponse)
async def download_by_id(
    file_id: UUID4, service: FileItemService = Depends(get_file_item_service)
):
    try:
        result = await service.download_by_id(file_id=file_id)
        return result
    except ApplicationException as e:
        return e.to_json_response()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return ApplicationException().to_json_response()


@router.delete("/{file_id}", response_model=FileItemRead)
async def delete_by_id(
    file_id: UUID4, service: FileItemService = Depends(get_file_item_service)
):
    try:
        result = await service.delete_by_id(file_id=file_id)
        return result
    except ApplicationException as e:
        return e.to_json_response()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return ApplicationException().to_json_response()


@router.patch("/", response_model=FileItemRead)
async def rename_by_id(
    dto: FileItemRename, service: FileItemService = Depends(get_file_item_service)
):
    try:
        result = await service.rename(dto=dto)
        return result
    except ApplicationException as e:
        return e.to_json_response()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return ApplicationException().to_json_response()
