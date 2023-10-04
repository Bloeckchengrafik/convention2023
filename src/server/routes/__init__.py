from fastapi import APIRouter

from .auth import auth_router
from .pipeline import pipeline_router
from .scan import scan_router

router = APIRouter()

router.include_router(pipeline_router, prefix="/pipeline", tags=["pipeline"])
router.include_router(scan_router, prefix="/scan", tags=["scan"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
