import asyncio
import logging

from server.driver import Driver
from server.driver.command import *


async def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)7s %(name)7s %(message)s")
    driver = Driver()
    driver.submit_command(LoadCommand(0))

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
