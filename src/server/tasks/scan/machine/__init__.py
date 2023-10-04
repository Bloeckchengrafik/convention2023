from server.tasks.scan.scanner import Scanner, ScannedSample


class MachineScanner(Scanner):
    async def run_scan(self) -> list[ScannedSample, ...]:
        raise NotImplementedError
