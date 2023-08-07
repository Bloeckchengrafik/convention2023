import cv2

from server.cv.utils import VertexNetwork2D


def find_line(image: cv2.Mat) -> VertexNetwork2D:
    height, _, _ = image.shape
    net = []

    # red threshold
    red_threshold = 75
    thresholder = cv2.threshold(image, red_threshold, 255, cv2.THRESH_BINARY)[1]
    bw = cv2.cvtColor(thresholder, cv2.COLOR_BGR2GRAY)
    preview = cv2.cvtColor(bw, cv2.COLOR_GRAY2BGR)
    preview = cv2.bitwise_not(preview)

    skipped = 0
    for i in range(0, height):
        # Search for the first and last red pixel in the row
        # If there are no red pixels, then we can skip this row
        red_pixels = cv2.findNonZero(bw[i])
        if red_pixels is None:
            skipped += 1
            continue
        # Add the first red pixel to the network
        first = red_pixels[0][0][1]
        last = red_pixels[-1][0][1]
        center = (first + last) / 2
        net.append([center, i])

    return VertexNetwork2D(net, preview)
