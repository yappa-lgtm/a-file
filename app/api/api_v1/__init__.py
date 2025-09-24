from fastapi import APIRouter

from core.config import settings

from .file_items import router as file_items_router
from .healthcheck import router as healthcheck_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(healthcheck_router, prefix=settings.api.v1.healthcheck)
router.include_router(file_items_router, prefix=settings.api.v1.file_items)
