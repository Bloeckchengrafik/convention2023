from enum import StrEnum


class JobStatus(StrEnum):
    """
    Enum for job status
    """
    PENDING = 'pending'
    PROCESSING = 'processing'
    CUTTING = 'cutting'
    DONE = 'done'
    ERROR = 'error'
