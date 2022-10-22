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
    contours = detect_contours(processed_image, downsized_image, debug=debug)
    rectangular_contours = filter_rectangular_contours(
        downsized_image,
        contours,
        debug=debug,
    )
    big_contours = filter_internal_contours(
        downsized_image,
        rectangular_contours,
        debug=debug,
    )
    internal_contours = filter_external_contour(
        downsized_image,
        big_contours,
        debug=debug,
    )
    largest_contours = filter_largest_contours(
        downsized_image,
        internal_contours,
        debug=debug,
    )
    if not largest_contours:
        raise NoContourFoundError("No valid contour was found")
    return approximate_contour(largest_contours[0])


def approximate_contour(contour: np.ndarray) -> np.ndarray:
    perimeter = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.032 * perimeter, True)


def filter_rectangular_contours(
    original_image: np.ndarray,
    contours: list[np.ndarray],
    debug: bool = False,
) -> list[np.ndarray]:
    logger.debug("Filtering non-rectangular contours...")
    rectangular_contours = list(
        filter(lambda contour: len(approximate_contour(contour)) == 4, contours)
    )
    contours_detected_image = cv2.drawContours(
        original_image.copy(), rectangular_contours, -1, (0, 255, 0), 3
    )
    debug_show(contours_detected_image, debug=debug)
    return rectangular_contours


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


def filter_internal_contours(
    original_image: np.ndarray,
    contours: list[np.ndarray],
    debug: bool = False,
) -> list[np.ndarray]:
    logger.debug("Filtering very small internal contours...")
    ordered = sorted(contours, key=cv2.contourArea)
    final_contours: list[np.ndarray] = []
    for index, contour in enumerate(ordered):
        if index == len(contours) - 1 and not final_contours:
            final_contours.append(contour)
        else:
            if contour_not_too_small(original_image, contour):
                final_contours.append(contour)
    image_with_contours = cv2.drawContours(
        original_image.copy(), final_contours, -1, (0, 255, 0), 3
    )
    debug_show(image_with_contours, debug=debug)
    return final_contours


def filter_external_contour(
    original_image: np.ndarray,
    contours: list[np.ndarray],
    debug: bool = False,
) -> list[np.ndarray]:
    logger.debug("Filtering artificial external contour...")
    ordered = sorted(contours, key=cv2.contourArea, reverse=True)
    final_contours: list[np.ndarray] = []
    for index, contour in enumerate(ordered):
        if index == len(contours) - 1 and not final_contours:
            final_contours.append(contour)
        else:
            if contour_not_too_big(original_image, contour):
                final_contours.append(contour)
    image_with_contours = cv2.drawContours(
        original_image.copy(), final_contours, -1, (0, 255, 0), 3
    )
    debug_show(image_with_contours, debug=debug)
    return final_contours


def contour_not_too_big(image: np.ndarray, contour: np.ndarray) -> bool:
    return cv2.contourArea(contour) <= (0.75 * image.shape[0] * image.shape[1])


def contour_not_too_small(image: np.ndarray, contour: np.ndarray) -> bool:
    return cv2.contourArea(contour) >= (0.1 * image.shape[0] * image.shape[1])


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
