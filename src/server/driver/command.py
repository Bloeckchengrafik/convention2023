from asyncio import Queue


class DriverCommand:
    pass


class CommandHandler:
    def __init__(self):
        self.queue = []

    def submit_command(self, command: DriverCommand):
        self.queue.append(command)

    def pop_command(self) -> DriverCommand or None:
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)

    def commands_left(self) -> int:
        return len(self.queue)


class LoadCommand(DriverCommand):
    def __init__(self, layer):
        self.layer = layer


class HomeCutterCommand(DriverCommand):
    pass


class ActivateCutterCommand(DriverCommand):
    pass


class DeactivateCutterCommand(DriverCommand):
    pass


class DriveCommand(DriverCommand):
    def __init__(self, top, top_speed, bottom, bottom_speed, turn, turn_speed):
        super().__init__()
        self.top = top
        self.top_speed = top_speed
        self.bottom = bottom
        self.bottom_speed = bottom_speed
        self.turn = turn
        self.turn_speed = turn_speed

    def __repr__(self):
        return f"DriveCommand(top={self.top}, top_speed={self.top_speed}, bottom={self.bottom}, bottom_speed={self.bottom_speed}, turn={self.turn}, turn_speed={self.turn_speed})"


class WaitCommand(DriverCommand):
    pass
