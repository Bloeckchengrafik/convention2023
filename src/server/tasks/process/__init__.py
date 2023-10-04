import dataclasses
import cv2

from server.datastore import ScanImages, DbSession
from server.utils.asynctasks import AsyncTask
from concurrent.futures import ProcessPoolExecutor


@dataclasses.dataclass
class ProcessorBatchConfiguration:
    max_batch_size: int = 50


class BatchedImageProcessor(AsyncTask):
    def __init__(self, images: list[ScanImages, ...], config=ProcessorBatchConfiguration()):
        self.images = images
        self.config = config

    async def impl(self):
        # Split images into batches
        # For each batch, process the images
        # Return the processed images
        batches = []
        for i in range(0, len(self.images), self.config.max_batch_size):
            batches.append(self.images[i:i + self.config.max_batch_size])

        processes = []
        for batch in batches:
            processes.append(ImageBatchProcessorProcess(batch))

        with ProcessPoolExecutor() as executor:
            results = executor.map(lambda process: process.run(), processes)

        with DbSession() as session:
            pass


class ImageBatchProcessorProcess:
    def __init__(self, batch: list[ScanImages, ...]):
        super().__init__()
        self.batch = batch
        self.processor = ImageProcessor()

    def run(self):
        pass


class ImageProcessor:
    @staticmethod
    async def process(image_left: str, image_right: str):
        left = cv2.imread(image_left)
        right = cv2.imread(image_right)

        vertices_left = find_line(left)
        vertices_right = find_line(right)

        vertices_left.plot()
        vertices_right.plot()

