from fastapi import APIRouter

from .pipeline import pipeline_router

router = APIRouter()

router.include_router(pipeline_router, prefix="/pipeline", tags=["pipeline"])
