import asyncio
from logging import getLogger
from platformio.device.finder import SerialPortFinder

from server.driver.command import CommandHandler, LoadCommand, HomeCutterCommand, ActivateCutterCommand, \
    DeactivateCutterCommand, WaitCommand, DriveCommand
from server.driver.io import Io
from swarm import *


class Driver(CommandHandler):
    def __init__(self):
        super().__init__()

        # run mainloop in current thread
        asyncio.create_task(self.mainloop())
        self.logger = getLogger("driver")
        spf = SerialPortFinder()
        self.logger.info("Searching for ftSwarm")
        port = spf.find()
        if port is None:
            self.logger.error("No ftSwarm found")
            exit(1)

        self.logger.info("Found ftSwarm on " + port)
        self.swarm: FtSwarm = FtSwarm(port, debug=True)

    def wormfactor(self, mm):
        return int((mm / 5) * 200)

    async def mainloop(self):
        manualdrive = await self.swarm.get_digital_input(Io.ManualDrive)
        #scanner_stepper = await self.swarm.get_stepper(Io.Scanner.ScannerStepper)
        centerer_compresor = await self.swarm.get_motor(Io.Centerer.Compressor)
        centerer_magnetvalve = await self.swarm.get_motor(Io.Centerer.MagnetValve)
        cutter_endstop_upper = await self.swarm.get_digital_input(Io.Cutter.EndstopUpper)
        cutter_endstop_lower = await self.swarm.get_digital_input(Io.Cutter.EndstopLower)
        cutter_upper = await self.swarm.get_stepper(Io.Cutter.Upper)
        cutter_lower = await self.swarm.get_stepper(Io.Cutter.Lower)
        relais = await self.swarm.get_motor(Io.Cutter.Relais)
        #cutter_vchain = await self.swarm.get_stepper(Io.Cutter.VChain)
        cutter_vchain_endstop = await self.swarm.get_digital_input(Io.Cutter.VChainEndstop)
        cutter_rot = await self.swarm.get_stepper(Io.Cutter.Rotation)
        cutter_rot_endstop = await self.swarm.get_digital_input(Io.Cutter.RotationEndstop)

        while True:
            command = self.pop_command()
            if command is None:
                await asyncio.sleep(0.1)
                continue

            self.logger.info("Got command " + command.__class__.__name__)

            if isinstance(command, LoadCommand):
                #await self.load(centerer_compresor, centerer_magnetvalve, cutter_vchain)
                pass
            elif isinstance(command, HomeCutterCommand):

                lower_begin = await cutter_endstop_lower.get_value()
                upper_begin = await cutter_endstop_upper.get_value()
                await cutter_upper.set_speed(200)
                await cutter_lower.set_speed(200)
                await cutter_upper.set_distance(-4000, True)
                await cutter_lower.set_distance(-4000, True)

                if lower_begin:
                    await cutter_lower.run()
                if upper_begin:
                    await cutter_upper.run()

                lower_stopped = False
                upper_stopped = False
                while True:
                    if not await cutter_endstop_upper.get_value() and not upper_stopped:
                        await cutter_upper.stop()
                        upper_stopped = True
                    if not await cutter_endstop_lower.get_value() and not lower_stopped:
                        await cutter_lower.stop()
                        lower_stopped = True
                    if upper_stopped and lower_stopped:
                        break
                #await self.home_cutter(cutter_endstop_upper, cutter_upper, cutter_endstop_lower, cutter_lower,
                #                       cutter_vchain, cutter_vchain_endstop, cutter_rot, cutter_rot_endstop)
            elif isinstance(command, ActivateCutterCommand):
                await self.activate_cutter(relais)
            elif isinstance(command, DeactivateCutterCommand):
                await self.deactivate_cutter(relais)
            elif isinstance(command, WaitCommand):
                await self.wait(manualdrive)
            elif isinstance(command, DriveCommand):
                await self.drive(command, cutter_rot, cutter_upper, cutter_lower)

    async def sleep_with_progress(self, seconds):
        print(seconds)
        for i in range(int(seconds * 2)):
            self.logger.info("Sleeping " + str(seconds - i / 2))
            await asyncio.sleep(0.5)

    async def load(self, compressor: FtSwarmMotor, magnetvalve: FtSwarmMotor, vchain: FtSwarmStepper):
        await compressor.set_speed(255)
        await asyncio.sleep(1)
        await magnetvalve.set_speed(255)
        await vchain.set_speed(200)
        await vchain.set_distance(self.wormfactor(150), True)
        await vchain.run()

        await self.sleep_with_progress(self.wormfactor(155) / 200)

        await magnetvalve.set_speed(0)
        await asyncio.sleep(1)
        await compressor.set_speed(0)
        await vchain.set_distance(-self.wormfactor(80), True)
        await vchain.run()

        await self.sleep_with_progress(self.wormfactor(85) / 200)

    async def home_cutter(self, endstop_upper: FtSwarmDigitalInput, upper: FtSwarmStepper,
                          endstop_lower: FtSwarmDigitalInput, lower: FtSwarmStepper,
                          vchain: FtSwarmStepper, endstop_vchain: FtSwarmDigitalInput,
                          rot: FtSwarmStepper, endstop_rot: FtSwarmDigitalInput):
        await vchain.set_speed(300)

        lower_begin = await endstop_lower.get_value()
        upper_begin = await endstop_upper.get_value()
        await upper.set_speed(200)
        await lower.set_speed(200)
        await upper.set_distance(-4000, True)
        await lower.set_distance(-4000, True)

        if lower_begin:
            await lower.run()
        if upper_begin:
            await upper.run()

        lower_stopped = False
        upper_stopped = False
        while True:
            if not await endstop_upper.get_value() and not upper_stopped:
                await upper.stop()
                upper_stopped = True
            if not await endstop_lower.get_value() and not lower_stopped:
                await lower.stop()
                lower_stopped = True
            if upper_stopped and lower_stopped:
                break

        await vchain.set_distance(-1100000, True)
        await vchain.run()

        while True:
            if not await endstop_vchain.get_value():
                break
            await asyncio.sleep(0.1)

        await vchain.stop()

        await rot.set_speed(50)
        await rot.set_distance(-10000, True)
        await rot.run()

        while True:
            if not await endstop_rot.get_value():
                break
            await asyncio.sleep(0.1)

        await rot.stop()

    async def activate_cutter(self, relais: FtSwarmMotor):
        await relais.set_speed(255)

    async def deactivate_cutter(self, relais: FtSwarmMotor):
        await relais.set_speed(0)

    async def wait(self, manualdrive: FtSwarmDigitalInput):
        print("Waiting for click")
        while True:
            if not await manualdrive.get_value():
                break
            await asyncio.sleep(0.1)

        print("Click detected")

    async def drive(self, command: DriveCommand, stepper_rot: FtSwarmStepper, stepper_upper: FtSwarmStepper,
                    stepper_lower: FtSwarmStepper):
        print(command)
        await stepper_rot.set_speed(50)
        await stepper_rot.set_distance(command.turn, True)

        await stepper_upper.set_speed(command.top_speed)
        await stepper_upper.set_distance(command.top, True)

        await stepper_lower.set_speed(command.bottom_speed)
        await stepper_lower.set_distance(command.bottom, True)

        if command.turn_speed != 0:
            await stepper_rot.run()
        if command.top:
            await stepper_upper.run()
        if command.bottom:
            await stepper_lower.run()

        await asyncio.sleep(max(command.top, command.bottom, command.turn) / 200)
