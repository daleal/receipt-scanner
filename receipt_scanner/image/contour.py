from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.errors import NoContourFoundError

logger = getLogger(__name__)


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


def find_contour(
    processed_image: np.ndarray, downsized_image: np.ndarray, debug: bool = False
) -> np.ndarray:
    contours = detect_contours(processed_image, downsized_image)
    largest_contours = filter_largest_contours(downsized_image, contours, debug=debug)
    best_contour = find_best_rectangular_contour(largest_contours)
    return approximate_contour(best_contour)


def approximate_contour(contour: np.ndarray) -> np.ndarray:
    perimeter = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.032 * perimeter, True)


def find_best_rectangular_contour(contours: list[np.ndarray]) -> np.ndarray:
    logger.debug("Searching for the best contour...")
    for contour in contours:
        contour_approximation = approximate_contour(contour)
        if len(contour_approximation) == 4:
            return contour_approximation
    raise NoContourFoundError("No valid contour was found")


def filter_largest_contours(
    original_image: np.ndarray,
    contours: list[np.ndarray],
    amount: int = 3,
    debug: bool = False,
) -> list[np.ndarray]:
    logger.debug("Filtering smaller contours...")
    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:amount]
    image_with_largest_contours = cv2.drawContours(
        original_image.copy(), largest_contours, -1, (0, 255, 0), 3
    )
    debug_show(image_with_largest_contours, debug=debug)
    return largest_contours


def detect_contours(
    edged_image: np.ndarray, original_image: np.ndarray, debug: bool = False
) -> list[np.ndarray]:
    logger.debug("Detecting contours...")
    contours, _ = cv2.findContours(edged_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_detected_image = cv2.drawContours(
        original_image.copy(), contours, -1, (0, 255, 0), 3
    )
    debug_show(contours_detected_image, debug=debug)
    return list(contours)
