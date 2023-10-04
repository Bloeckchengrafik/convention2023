from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.datastore import get_db, ScanSample
from server.datastore.enum import DatasetType
from server.tasks.scan import ScannerFactory

scan_router = APIRouter()


@scan_router.get("/p/{pipeline_id}")
def scans_by_pipeline(pipeline_id: int, db: Session = Depends(get_db)):
    return db.query(ScanSample).order_by(ScanSample.timestamp).filter(ScanSample.pipeline_id == pipeline_id).all()[::-1]


@scan_router.get("/id/{scan_id}")
def scan_by_id(scan_id: int, db: Session = Depends(get_db)):
    return db.query(ScanSample).filter(ScanSample.id == scan_id).first()


@scan_router.get("/p/{pipeline_id}/run")
async def new(pipeline_id: int, dataset: DatasetType):
    ScannerFactory(
        pipeline_id=pipeline_id,
        dataset=dataset
    )()
