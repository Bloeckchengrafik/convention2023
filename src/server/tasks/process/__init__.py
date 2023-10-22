import asyncio
import json
import logging
import math

from pyvista.plotting.themes import Theme

from server.datastore import ScanSample, ScanCoordinates, SessionLocal, Pipeline, PipelineStatus
from server.utils.asynctasks import AsyncTask

import pyvista


class SampleProcessor(AsyncTask):
    async def impl(self, samples: list[ScanSample]):
        """
        This function takes a list of ScanSamples and processes them into a 3d mesh using the following algorithm:
        1. Sort the samples by layer_nr
        2. Find the samples that are in a line on top of each other (different layer_nr but same rotation)
        3. build a line between these samples
        4. build a line between the points in the line and the next line
        """
        verticies: list[tuple[float, float, float]] = []
        samples.sort(key=lambda x: x.layer_nr)
        logger = logging.getLogger("SampleProcessor")

        layer_out_of_range = []

        for sample in samples:
            if sample.sample > 180:
                layer_out_of_range.append(sample.layer_nr)

            sample.sample = 180 - sample.sample

        rot_dict = {}

        for sample in samples:
            if sample.layer_nr in layer_out_of_range:
                logger.info("Ignoring sample %s because it is out of range", sample.id)
                continue

            if sample.rotation in rot_dict:
                rot_dict[sample.rotation].append(sample)
            else:
                rot_dict[sample.rotation] = [sample]

        for rotation in rot_dict:
            rot_dict[rotation].sort(key=lambda x: x.layer_nr)

        verticies = []
        edges = []
        faces = []

        height = list(set([sample.layer_nr for sample in samples]))

        for rotation in rot_dict:
            for sample in rot_dict[rotation]:
                z = sample.layer_nr * 30
                rotation_radiants = sample.rotation
                distance_from_outside = sample.sample
                distance_from_center = 180 - distance_from_outside
                x = math.cos(rotation_radiants) * distance_from_center
                y = math.sin(rotation_radiants) * distance_from_center

                verticies.append((x, y, z))

        # a line through all the verticies
        for i in range(len(verticies) - 1):
            # not for the last vertex per layer
            if i % len(height) != len(height) - 1:
                edges.append((i, i + 1))

        # a line between the verticies of the same layer
        for i in range(len(verticies) - len(height)):
            edges.append((i, i + len(height)))

        # close the loop (the layers are full circles)
        # we got the following issue:
        # the last vertex of a layer is not connected to the first vertex of the same layer
        for layer_nr in range(len(height)):
            # get the first vertex of the layer
            first_vertex = layer_nr
            # get the last vertex of the layer
            rotations = len(rot_dict) - 1
            last_vertex = len(height) * rotations + layer_nr
            edges.append((last_vertex, first_vertex))

        # faces!!!!
        for i in range(len(verticies) - len(height) - 1):
            faces.append((i, i + 1, i + len(height) + 1, i + len(height)))

        # close the loop (the layers are full circles)
        # we got the following issue:
        # the last vertex of a layer is not connected to the first vertex of the same layer
        for layer_nr in range(len(height)):
            # get the first vertex of the layer
            first_vertex = layer_nr
            # get the last vertex of the layer
            rotations = len(rot_dict) - 1
            last_vertex = len(height) * rotations + layer_nr
            if layer_nr != len(height) - 1:
                faces.append((last_vertex, first_vertex, first_vertex + 1, last_vertex + 1))

        # Add a new vertex at 0 0 0
        verticies.append((0, 0, 0))
        # add a new vertex at 0 0 (last layer)
        verticies.append((0, 0, height[-1] * 30))

        # for the first of the added verticies: draw a line to all the verticies of the first layer
        # for the second of the added verticies: draw a line to all the verticies of the last layer
        i = 0
        for vertex in verticies:
            if i % len(height) == 0:
                edges.append((len(verticies) - 2, i))
                faces.append((len(verticies) - 2, i, i + 1))
            if i % len(height) == len(height) - 1:
                edges.append((len(verticies) - 1, i))
                faces.append((len(verticies) - 1, i, i - 1))
            i += 1

        # The face connectivity array. This array requires padding indicating the number of points in a face.
        # For example, the two faces [0, 1, 2] and [2, 3, 4, 5] will be represented as [3, 0, 1, 2, 4, 2, 3, 4, 5].
        faces_for_viz = []
        for i in range(len(faces)):
            faces_for_viz.append(len(faces[i]))
            for j in range(len(faces[i])):
                faces_for_viz.append(faces[i][j])

        # The line connectivity array. Like faces, this array requires padding indicating the number of points in a
        # line segment. For example, the two line segments [0, 1] and [1, 2, 3, 4] will be represented
        # as [2, 0, 1, 4, 1, 2, 3, 4].
        lines = []
        for i in range(len(edges)):
            lines.append(2)
            lines.append(edges[i][0])
            lines.append(edges[i][1])

        theme = Theme()
        theme.transparent_background = True

        mesh = pyvista.PolyData(verticies, lines=lines, faces=faces_for_viz)
        mesh.plot(off_screen=True, screenshot="mesh.png", theme=theme)

        with open("rot_dict.data", "w") as f:
            for key in rot_dict:
                f.write("%s\n" % key)
                for item in rot_dict[key]:
                    f.write("%s %s\n" % (item.sample, item.layer_nr))
                f.write("\n")
            await asyncio.sleep(0.1)

        database = SessionLocal()
        job_id = samples[0].pipeline_id
        dbscan_coords = []
        for vertex in verticies:
            coords = ScanCoordinates()
            coords.pipeline_id = job_id
            coords.x = vertex[0]
            coords.y = vertex[1]
            coords.z = vertex[2]
            dbscan_coords.append(coords)

        database.add_all(dbscan_coords)

        pipeline = database.query(Pipeline).filter(Pipeline.id == job_id).first()
        pipeline.status = PipelineStatus.BUILDING
        database.commit()
        database.close()
