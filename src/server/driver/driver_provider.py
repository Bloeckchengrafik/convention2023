import asyncio
import threading
import time
from typing import Annotated

from fastapi import Depends

from server.driver import Driver


class DriverProvider:
    def __init__(self):
        self._driver = None

    def resolve(self) -> Driver:
        if self._driver is None:
            # create driver in a new thread
            async def create_driver():
                from server.driver import Driver
                self._driver = Driver()

                while True:
                    await asyncio.sleep(1)

            threading.Thread(target=asyncio.run, args=(create_driver(),)).start()
            while self._driver is None:
                time.sleep(0.1)
                print(".", end="", flush=True)

        return self._driver


provider = DriverProvider()


def get_driver() -> Driver:
    return provider.resolve()


DriverDep = Annotated[Driver, Depends(get_driver)]
