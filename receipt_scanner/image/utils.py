import cv2
import numpy as np


def approximate_contour(contour: np.ndarray) -> np.ndarray:
    perimeter = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.032 * perimeter, True)


def contour_to_rect(contour: np.ndarray, resize_ratio: float) -> np.ndarray:
    points = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    # top-left point has the smallest sum
    # bottom-right has the largest sum
    axis_values_sum = points.sum(axis=1)
    rect[0] = points[np.argmin(axis_values_sum)]
    rect[2] = points[np.argmax(axis_values_sum)]
    # compute the difference between the points:
    # the top-right will have the minumum difference
    # the bottom-left will have the maximum difference
    axis_values_difference = np.diff(points, axis=1)
    rect[1] = points[np.argmin(axis_values_difference)]
    rect[3] = points[np.argmax(axis_values_difference)]
    return rect / resize_ratio


def wrap_perspective(image: np.ndarray, rect: np.ndarray):
    (top_left, top_right, bottom_right, bottom_left) = rect

    top_width = np.sqrt(
        ((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2)
    )
    bottom_width = np.sqrt(
        ((bottom_right[0] - bottom_left[0]) ** 2)
        + ((bottom_right[1] - bottom_left[1]) ** 2)
    )

    left_height = np.sqrt(
        ((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2)
    )
    right_height = np.sqrt(
        ((top_right[0] - bottom_right[0]) ** 2)
        + ((top_right[1] - bottom_right[1]) ** 2)
    )

    max_width = max(int(bottom_width), int(top_width))
    max_height = max(int(right_height), int(left_height))

    destination = np.array(
        [
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1],
        ],
        dtype="float32",
    )
    perspective_transform_matrix = cv2.getPerspectiveTransform(rect, destination)
    return cv2.warpPerspective(
        image, perspective_transform_matrix, (max_width, max_height)
    )
