from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from server.datastore import Pipeline, PipelineStatus, get_db, ScanSample
from server.driver.driver_provider import get_driver
from server.tasks.cut import CutTask
from server.tasks.process import SampleProcessor
from server.tasks.slice import Slicer

pipeline_router = APIRouter()


@pipeline_router.get("/")
def process_index(db: Session = Depends(get_db)):
    return db.query(Pipeline).order_by(Pipeline.timestamp).all()[::-1]


@pipeline_router.get("/id/{job_id}")
def process_index(job_id: int, db: Session = Depends(get_db)):
    return {
        **db.query(Pipeline).filter(Pipeline.id == job_id).first().__dict__,
        "sample_count": len(db.query(ScanSample).filter(ScanSample.pipeline_id == job_id).all())
    }


@pipeline_router.get("/id/{job_id}/samples")
def process_index(job_id: int, db: Session = Depends(get_db)):
    return db.query(ScanSample).filter(ScanSample.pipeline_id == job_id).all()


@pipeline_router.get("/id/{job_id}/complete_early")
def process_index(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Pipeline).filter(Pipeline.id == job_id).first()
    job.status = PipelineStatus.DONE
    db.commit()
    return job


@pipeline_router.get("/id/{job_id}/cancel")
def process_index(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Pipeline).filter(Pipeline.id == job_id).first()
    job.status = PipelineStatus.ERROR
    db.commit()
    return job


@pipeline_router.get("/id/{job_id}/process")
def process_index(job_id: int, db: Session = Depends(get_db)):
    samples = db.query(ScanSample).filter(ScanSample.pipeline_id == job_id).all()
    SampleProcessor()(samples)


@pipeline_router.get("/id/{job_id}/cut")
async def process_index(job_id: int, driver=Depends(get_driver)):
    CutTask()(driver, job_id)


@pipeline_router.get("/id/{job_id}/slice")
def process_index(job_id: int, db: Session = Depends(get_db)):
    Slicer()()


@pipeline_router.get("/current_preview_image")
def process_index():
    return FileResponse("mesh.png")


@pipeline_router.get("/status/{status}")
def process_index(status: PipelineStatus, db: Session = Depends(get_db)):
    return db.query(Pipeline).filter(Pipeline.status == status).all()


@pipeline_router.get("/new")
def new(db: Session = Depends(get_db)):
    new_job = Pipeline(status=PipelineStatus.PENDING)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job
