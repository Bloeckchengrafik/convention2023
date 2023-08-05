from fastapi import APIRouter

from .pipeline import pipeline_router
from .scan import scan_router

router = APIRouter()

router.include_router(pipeline_router, prefix="/pipeline", tags=["pipeline"])
router.include_router(scan_router, prefix="/scan", tags=["scan"])
