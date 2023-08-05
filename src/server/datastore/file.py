import os

from ulid import ULID


class FileStorageManagement:
    def __init__(self):
        # Make sure there is a data/ directory
        os.makedirs("data", exist_ok=True)
        self.latest_files = {}

    def provision(self, extension: str, identifier: str = None) -> tuple[ULID, str]:
        file_ulid = ULID()
        path = f"data/{identifier or ''}{file_ulid}.{extension}"
        self.latest_files[str(file_ulid)] = path
        return file_ulid, path

    def get_resource(self, file_ulid: ULID) -> str:
        if file_ulid not in self.latest_files:
            # search for file in data/ directory
            for file in os.listdir("data"):
                if file.split(".")[0].endswith(str(file_ulid)):
                    self.latest_files[str(file_ulid)] = f"data/{file}"
                    break
            else:
                raise FileNotFoundError(f"Could not find file with ULID {file_ulid}")
        return self.latest_files[file_ulid]


storage_management = FileStorageManagement()


class Resource:
    """
    This is a way to easily open a file in a context manager.
    """

    def __init__(self, mode: str, file_ulid_or_extension: ULID | str):
        file_ulid = file_ulid_or_extension
        if isinstance(file_ulid_or_extension, str):
            file_ulid, _ = storage_management.provision(file_ulid_or_extension)

        self.file_ulid = file_ulid
        self.path = storage_management.get_resource(file_ulid)
        self.file = None
        self.mode = mode

    def __enter__(self):
        self.file = open(self.path, "rb")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
