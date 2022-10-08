from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.contour import contour_to_rect
from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class PerspectiveWrapperFilter(Filter):
    def __init__(
        self,
        contour: np.ndarray,
        resize_ratio: float,
        debug: bool = False,
    ) -> None:
        self.contour = contour
        self.resize_ratio = resize_ratio
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'PerspectiveWrapperFilter'...")
        working_image = image.copy()
        contour_rect = contour_to_rect(self.contour, self.resize_ratio)
        wrapped_perspective_image = wrap_perspective(working_image, contour_rect)
        debug_show(wrapped_perspective_image, debug=self.debug)
        return wrapped_perspective_image


def wrap_perspective(image: np.ndarray, rect: np.ndarray) -> np.ndarray:
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
