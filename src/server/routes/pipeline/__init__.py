from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.datastore import Pipeline, JobStatus, get_db

pipeline_router = APIRouter()


@pipeline_router.get("/")
def process_index(db: Session = Depends(get_db)):
    return db.query(Pipeline).order_by(Pipeline.timestamp).all()[::-1]


@pipeline_router.get("/id/{job_id}")
def process_index(job_id: int, db: Session = Depends(get_db)):
    return db.query(Pipeline).filter(Pipeline.id == job_id).first()


@pipeline_router.get("/status/{status}")
def process_index(status: JobStatus, db: Session = Depends(get_db)):
    return db.query(Pipeline).filter(Pipeline.status == status).all()


@pipeline_router.get("/new")
def new(db: Session = Depends(get_db)):
    new_job = Pipeline(status=JobStatus.PENDING)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job
