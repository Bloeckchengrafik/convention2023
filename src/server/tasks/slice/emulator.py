import math


class Emulator:
    def __init__(self, length_wire, steps, vmax_stepper):
        self.length_wire = length_wire
        self.steps = steps  # Steps for one full rotation of the stepper motor
        self.wormscrew_factor = 5  # Movement in mm for one full rotation
        self.vmax = vmax_stepper
        self.low = 77+23
        self.steps_low = self.low / self.wormscrew_factor * self.steps
        self.high = 77+23
        self.steps_high = self.high / self.wormscrew_factor * self.steps
        self.rotation_teeth = 58 / 10  # Teeth of both gears in comparison
        self.rotation = 0

    def angle_calculation(self, angle):
        d = self.length_wire * math.cos(math.radians(angle))
        return d

    def position_low(self, distance, angle):
        d = distance - 0.5 * self.length_wire * math.cos(math.radians(angle))
        return d

    def position_high(self, distance, angle):
        d = self.position_low(distance, angle) + self.angle_calculation(angle)
        return d

    def position(self, distance, angle):
        return self.position_low(distance, angle), self.position_high(distance, angle)

    def dist_position(self, distance, angle):
        self.d_low = abs(self.low - self.position_low(distance, angle))
        if self.low > self.position_low(distance, angle):
            self.d_low = self.d_low * (-1)

        self.d_high = abs(self.high - self.position_high(distance, angle))
        if self.high > self.position_high(distance, angle):
            self.d_high = self.d_high * (-1)

        self.low = self.position_low(distance, angle)
        self.high = self.position_high(distance, angle)
        return self.d_low, self.d_high

    def dist_high(self, distance, angle):
        self.d_high = abs(self.high - self.position_high(distance, angle))
        if self.high > self.position_high(distance, angle):
            self.d_high = self.d_high * (-1)
        self.high = self.position_high(distance, angle)
        return self.d_high

    def dist_low(self, distance, angle):
        self.d_low = abs(self.low - self.position_low(distance, angle))
        if self.low > self.position_low(distance, angle):
            self.d_low = self.d_low * (-1)
        self.low = self.position_low(distance, angle)
        return self.d_low

    def steps_calc(self, distance):
        steps_c = distance / 5 * self.steps
        steps_c = round(steps_c)
        return steps_c

    def next_cutter_step(self, distance, angle, rotation):
        travel_time = 0
        v_low = 0
        v_high = 0
        angle = self.angle_recalculation(angle)
        low = self.steps_calc(self.dist_low(distance, angle))

        if round(self.steps_low) * low < 0:
            if low < 0:
                low = low - 5 / 200 * self.steps

            if low > 0:
                low = low + 5 / 200 * self.steps
        high = self.steps_calc(self.dist_high(distance, angle))

        if round(self.steps_high) * high < 0:
            if high < 0:
                high = high - 5 / 200 * self.steps
            if high > 0:
                high = high + 5 / 200 * self.steps
        self.steps_high = self.high
        self.steps_low = self.low
        travel_time = low / self.vmax
        v_low = self.vmax
        v_high = self.vmax
        if self.steps_high < self.steps_low:
            v_low = self.vmax
            v_high = self.steps_high / self.steps_low * self.vmax
            travel_time = low / self.vmax

        if self.steps_high > self.steps_low:
            v_high = self.vmax
            v_low = self.steps_low / self.steps_high * self.vmax
            travel_time = high / self.vmax

        rot = self.rotation_steps(rotation)

        if not travel_time == 0:
            v_rot = rot / travel_time

        else:
            v_rot = self.vmax

        return abs(low), round(v_low), abs(high), round(v_high), abs(rot), round(v_rot)

    def angle_recalculation(self, angle):
        angle = angle * (-1)
        if angle < 0:
            angle = 180 + angle

        return angle

    def rotation_steps(self, angle):
        steps_full = self.rotation_teeth * self.steps
        steps = angle / 360 * steps_full
        if self.rotation > steps:
            steps = (-1) * abs(steps - self.rotation)

        elif self.rotation < steps:
            steps = abs(self.rotation - steps)

        elif self.rotation == steps:
            steps = 0

        self.rotation = angle / 360 * steps_full
        return round(steps)


if __name__ == '__main__':
    emu = Emulator(40, 200, 200)
    print(emu.next_cutter_step(6, 90, 1.8))
    print(emu.next_cutter_step(6, 90, 1.8*2))
