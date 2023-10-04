from enum import StrEnum


class PipelineStatus(StrEnum):
    """
    Enum for job status
    """
    PENDING = 'pending'
    PROCESSABLE = 'processable'
    PROCESSING = 'processing'
    CUTTING = 'cutting'
    DONE = 'done'
    ERROR = 'error'


class DatasetType(StrEnum):
    """
    Enum for dataset type
    """
    SCAN = 'machine'
    TEST = 'test'

