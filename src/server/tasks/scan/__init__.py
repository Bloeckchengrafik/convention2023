from server.datastore import DbSession, Pipeline
from server.datastore.enum import DatasetType, PipelineStatus
from server.tasks.scan.machine import MachineScanner
from server.tasks.scan.test import TestScanner
from server.utils.asynctasks import AsyncTask


class ScannerFactory(AsyncTask):
    def __init__(self, pipeline_id: int, dataset: DatasetType):
        self.pipeline_id = pipeline_id
        self.dataset = dataset

    async def impl(self):
        images = await self.get_scanner_cls()(self.pipeline_id).run_scan()
        # Save images to database
        with DbSession() as db:
            db.add_all([image.into_db(self.pipeline_id) for image in images])
            db.commit()
            # Get pipeline
            pipeline: Pipeline = db.query(Pipeline).filter(Pipeline.id == self.pipeline_id).first()
            # Update pipeline status
            pipeline.status = PipelineStatus.PROCESSABLE
            db.commit()

    def get_scanner_cls(self) -> type[MachineScanner, TestScanner]:
        match self.dataset:
            case DatasetType.TEST:
                return TestScanner
            case DatasetType.SCAN:
                return MachineScanner

