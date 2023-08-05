import shutil
from math import pi

from server.datastore.enum import ScannerPosition
from server.datastore.file import storage_management
from server.tasks.scan.scanner import Scanner, ScannerImage


class TestScanner(Scanner):
    async def run_scan(self) -> list[ScannerImage, ...]:
        """
        This is a test scanner that uses images from testdata/scanner
        """

        real_path_right = "testdata/scanner/right.png"
        real_path_left = "testdata/scanner/left.png"

        images = []

        for i in range(0, 360, self.resolution):
            # One left and one right
            ulid_l, path_l = storage_management.provision("png", f"p{self.pipeline_id}i{i}left.")
            ulid_r, path_r = storage_management.provision("png", f"p{self.pipeline_id}i{i}right.")
            shutil.copy(real_path_left, path_l)
            shutil.copy(real_path_right, path_r)

            phi_degrees = i
            phi_rad = phi_degrees * pi / 180
            theta_rad = 0
            gamma_deg = 45
            gamma_rad = gamma_deg * pi / 180

            images.append(ScannerImage(
                phi=phi_rad,
                theta=theta_rad,
                gamma=gamma_rad,
                position=ScannerPosition.LEFT,
                image=ulid_l
            ))

            images.append(ScannerImage(
                phi=phi_rad,
                theta=theta_rad,
                gamma=gamma_rad,
                position=ScannerPosition.RIGHT,
                image=ulid_r
            ))

        return images
