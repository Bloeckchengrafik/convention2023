import abc
import dataclasses

from ulid import ULID

from server.datastore import ScanImages
from server.datastore.enum import ScannerPosition


@dataclasses.dataclass
class ScannerImage:
    """
    Dataclass for a single image from a scanner

    Imagine a plane with the origin at the center of the scanner.
    Phi is the angle from the x-axis to the red line (in radians).
    Theta is the vertical angle from the x-y plane to the camera (in radians). Positive is up.
    Gamma is the deviation angle for a specific camera (in radians). Always positive.
    """
    phi: float
    theta: float
    gamma: float
    position: ScannerPosition
    image: ULID

    def into_db(self, pipeline_id: int) -> ScanImages:
        return ScanImages(
            phi=self.phi,
            theta=self.theta,
            gamma=self.gamma,
            position=self.position,
            image=str(self.image),
            pipeline_id=pipeline_id
        )


class Scanner(abc.ABC):
    def __init__(self, pipeline_id: int, resolution: int):
        self.pipeline_id = pipeline_id
        self.resolution = resolution

    @abc.abstractmethod
    async def run_scan(self) -> list[ScannerImage, ...]:
        pass
