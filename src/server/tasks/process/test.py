import asyncio

from server.tasks.process import ImageProcessor

if __name__ == '__main__':
    image_processor = ImageProcessor()
    asyncio.run(image_processor.process("../../../../testdata/scanner/left.png",
                                        "../../../../testdata/scanner/right.png"))
