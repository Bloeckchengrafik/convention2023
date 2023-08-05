from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.datastore import Pipeline, PipelineStatus, get_db

pipeline_router = APIRouter()


@pipeline_router.get("/")
def process_index(db: Session = Depends(get_db)):
    return db.query(Pipeline).order_by(Pipeline.timestamp).all()[::-1]


@pipeline_router.get("/id/{job_id}")
def process_index(job_id: int, db: Session = Depends(get_db)):
    return db.query(Pipeline).filter(Pipeline.id == job_id).first()

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
