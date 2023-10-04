import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime, Enum, ForeignKey, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from server.datastore.enum import PipelineStatus

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Pipeline(Base):
    __tablename__ = "pipeline"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Enum(PipelineStatus))

    samples = relationship("ScanSample", back_populates="pipeline")


class ScanSample(Base):
    __tablename__ = "scan_samples"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey(Pipeline.id))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    rotation = Column(Float)
    layer_nr = Column(Integer)
    sample = Column(Float)

    pipeline = relationship("Pipeline", back_populates="samples")


def init_database():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DbSession:
    """
    Context manager for database sessions
    """

    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
