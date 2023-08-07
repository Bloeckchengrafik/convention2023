import cv2
import numpy as np
import matplotlib.pyplot as plt

from server.linalg.Vecmath import Vector2


class VertexNetwork2D:
    """
    A network of verticies in 2D space. ("A Line with extra steps")
    """
    def __init__(self, verticies: np.ndarray, background_image: cv2.Mat = None):
        self.model = verticies
        self.background_image = background_image

    def simplify(self, tolerance: float):
        """
        Simplifies the network by removing verticies that are within a certain distance of a
        line between two other verticies, so that the network is less complex but still
        represents the same shape (roughly).
        """
        pass_is_empty = len(self.model) <= 2
        while not pass_is_empty:
            pass_is_empty = True
            for i in range(1, len(self.model) - 1):
                left = self.model[i - 1]
                middle = self.model[i]
                right = self.model[i + 1]

                left = Vector2(left[0], left[1])
                middle = Vector2(middle[0], middle[1])
                right = Vector2(right[0], right[1])

                line_distance = middle.distance_to_line(left, right)
                if line_distance < tolerance:
                    self.model = np.delete(self.model, i, 0)
                    pass_is_empty = False
                    break

    def plot(self):
        # We need to plot the verticies as multiple line segments
        # We can do this by plotting each line segment individually
        plt.style.use('_mpl-gallery-nogrid')
        fig, ax = plt.subplots()

        if self.background_image is not None:
            ax.imshow(self.background_image, cmap="gray", interpolation="bicubic")

        for i in range(len(self.model) - 1):
            left = self.model[i]
            right = self.model[i + 1]

            ax.plot([left[0], right[0]], [left[1], right[1]], color="green")

        plt.show()

