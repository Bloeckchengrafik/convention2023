import asyncio
import logging

from server.datastore import DbSession, Pipeline, PipelineStatus
from server.driver import Driver
from server.driver.command import *
from server.utils.asynctasks import AsyncTask


class CutTask(AsyncTask):
    def progress_bar(self, commands_max, commands_current):
        bar_length = 20
        progress = commands_current / commands_max
        bar = "█" * int(bar_length * progress) + "-" * int(bar_length * (1 - progress))
        print(f"[{bar}] {commands_current}/{commands_max}")

    async def impl(self, driver: Driver):
        layers = 0
        commands = []
        layer_commands = []
        with open("stepper_commands.hcode", "r") as f:
            for line in f.readlines():
                if line == "\n":
                    layers += 1
                    commands.append(layer_commands)
                    layer_commands = []
                else:
                    layer_commands.append(DriveCommand(*[int(x) for x in line.strip().split(" ")]))

        i = 0
        for layer in range(layers):
            driver.submit_command(HomeCutterCommand())
            i += 1
            driver.submit_command(WaitCommand())
            i += 1
            # driver.submit_command(LoadCommand(layer))
            driver.submit_command(ActivateCutterCommand())
            i += 1
            for command in commands[layer]:
                driver.submit_command(command)
                i += 1
            driver.submit_command(DeactivateCutterCommand())
            i += 1

        while left := driver.commands_left():
            self.progress_bar(i, i - left)
            await asyncio.sleep(0.5)

        self.progress_bar(i, i)


async def main():
    driver = Driver()
    await CutTask().impl(driver)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)7s %(message)s")
    asyncio.run(main())
