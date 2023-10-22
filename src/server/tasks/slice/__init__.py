import logging

from server.tasks.slice import pyStl
from server.tasks.slice.emulator import Emulator
from server.utils.asynctasks import AsyncTask

import numpy as np
from numba import njit


@njit
def eq(a: list[int], b: list[int]) -> bool:
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False

    return True


@njit
def index_of(a: list[list[int]], b: list[int]) -> int:
    for i in range(len(a)):
        if eq(a[i], b):
            return i
    return -1


class Slicer(AsyncTask):
    async def impl(self):
        logger = logging.getLogger('slicer')
        logger.info('Slicing started')
        rot_dict = {}

        # open rot_dict.data
        with open('rot_dict.data', 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                measure = float(lines[i].strip())
                rot_dict[measure] = []
                while line := lines[i + 1].strip():
                    rot_dict[measure].append([float(x) for x in line.split(' ')])
                    i += 1
                rot_dict[measure].append([20.0, 7.0])
                i += 2

        layers = len(rot_dict[list(rot_dict.keys())[0]])
        logger.info(f'Layers: {layers}')
        layer_height_for_7_layers = layers / 6
        logger.info(f'Layer height for 7 layers: {layer_height_for_7_layers}')

        transposed_dict = [{} for _ in range(layers)]
        for measure in rot_dict:
            for i in range(layers):
                transposed_dict[int(i)][measure] = rot_dict[measure][i][0]

        samples_per_layer = len(transposed_dict[0])
        logger.info(f'Samples per layer: {samples_per_layer}')

        new_data = [{} for _ in range(200)]
        for angle, dp in enumerate(new_data):
            for layer in range(layers):
                # calculate measure by using the index of the layer and the angle (0-199 -> 0-360 -> rad)
                radiants_angle = angle / 200 * 2 * np.pi
                # get the nearest measure
                nearest_measure = min(transposed_dict[layer].keys(), key=lambda x: abs(x - radiants_angle))
                new_data[angle][layer] = transposed_dict[layer][nearest_measure]

        # resample for 7 cuts
        new_data_7 = [{} for _ in range(200)]
        for angle, dp in enumerate(new_data_7):
            old = new_data[angle]
            for layer in range(7):
                layer_height = layer * layer_height_for_7_layers
                below_measure = max([x for x in old.keys() if x <= layer_height])
                if len([x for x in old.keys() if x >= layer_height]) == 0:
                    new_data_7[angle][layer] = old[below_measure]
                    continue
                above_measure = min([x for x in old.keys() if x >= layer_height])
                diff = above_measure - below_measure

                if diff == 0:
                    new_data_7[angle][layer] = old[below_measure]
                    continue

                p = (layer_height - below_measure) / diff
                new_data_7[angle][layer] = old[below_measure] * (1 - p) + old[above_measure] * p

        # distance angle rotation
        layers_to_cut: list[list[tuple[int, int, float]]] = [[] for _ in range(6)]

        for angle in range(220):
            # get 0-1 1-2 2-3 3-4 4-5 5-6 6-7
            for layer in range(6):
                h0 = new_data_7[int(angle) % 200][layer]
                h1 = new_data_7[int(angle) % 200][layer + 1]

                distance_from_center = (((h0 + h1) / 2) / 180) * 30
                if h0 == h1:
                    angle = 90
                else:
                    angle = np.arctan(1 / np.abs(h0 - h1)) * 180 / np.pi

                layers_to_cut[layer].append((int(round(distance_from_center)), int(round(angle)), 360 / 200))

        stepper_commands = [[] for _ in range(3)]
        for layer in range(3):
            emulator = Emulator(33, 200, 200)
            rot = 0
            for distance, angle, rotation in layers_to_cut[layer]:
                if layer == 0:
                    angle = -80
                elif layer == 1:
                    angle = 90
                else:
                    angle = 80
                stepper_commands[layer].append(emulator.next_cutter_step(distance, angle, rot))
                rot += rotation

        # write to file
        with open('stepper_commands.hcode', 'w') as f:
            for layer in range(3):
                for command in stepper_commands[layer]:
                    f.write(
                        f'{int(command[0])} {int(command[1])} {int(command[2])} {int(command[3])} {int(command[4])} {int(command[5])}\n')
                f.write('\n')
        logger.info('Slicing finished')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)7s %(message)s')
    Slicer()()
