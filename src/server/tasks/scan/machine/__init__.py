from server.tasks.scan.scanner import Scanner, ScannerImage


class MachineScanner(Scanner):
    async def run_scan(self) -> list[ScannerImage, ...]:
        raise NotImplementedError
