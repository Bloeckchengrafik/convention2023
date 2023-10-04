import abc
import dataclasses

from ulid import ULID

from server.datastore import ScanSample


@dataclasses.dataclass
class ScannedSample:
    """
    Dataclass for a single image from a scanner

    Imagine a plane with the origin at the center of the scanner.
    Phi is the angle from the x-axis to the red line (in radians).
    Theta is the vertical angle from the x-y plane to the camera (in radians). Positive is up.
    Gamma is the deviation angle for a specific camera (in radians). Always positive.
    """
    rotation: float
    layer_nr: int
    sample: float

    def into_db(self, pipeline_id: int) -> ScanSample:
        return ScanSample(
            pipeline_id=pipeline_id,
            rotation=self.rotation,
            layer_nr=self.layer_nr,
            sample=self.sample
        )


class Scanner(abc.ABC):
    def __init__(self, pipeline_id: int):
        self.pipeline_id = pipeline_id

    @abc.abstractmethod
    async def run_scan(self) -> list[ScannedSample, ...]:
        pass
