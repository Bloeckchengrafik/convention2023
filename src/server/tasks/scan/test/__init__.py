import math

from server.tasks.scan.scanner import Scanner, ScannedSample


class TestScanner(Scanner):
    async def run_scan(self) -> list[ScannedSample, ...]:
        samples = []

        # Rotation is in radians
        for i in range(0, 1000):
            for layer in range(0, 7):
                samples.append(ScannedSample(
                    rotation=(i / 1000) * 2 * math.pi,
                    layer_nr=layer,
                    sample=20  # cm
                ))
        return samples
