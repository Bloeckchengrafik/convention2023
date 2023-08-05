from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.datastore import get_db, ScanImages
from server.datastore.enum import DatasetType
from server.tasks.scan import ScannerFactory

scan_router = APIRouter()

@scan_router.get("/p/{pipeline_id}")
def scans_by_pipeline(pipeline_id: int, db: Session = Depends(get_db)):
    return db.query(ScanImages).order_by(ScanImages.timestamp).filter(ScanImages.pipeline_id == pipeline_id).all()[::-1]

@scan_router.get("/id/{scan_id}")
def scan_by_id(scan_id: int, db: Session = Depends(get_db)):
    return db.query(ScanImages).filter(ScanImages.id == scan_id).first()

@scan_router.get("/p/{pipeline_id}/run")
async def new(pipeline_id: int, dataset: DatasetType, resolution: int):
    ScannerFactory(
        pipeline_id=pipeline_id,
        dataset=dataset,
        resolution=resolution
    )()
