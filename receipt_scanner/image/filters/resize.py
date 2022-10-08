from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class ResizeFilter(Filter):
    def __init__(self, resize_ratio: float) -> None:
        self.resize_ratio = resize_ratio

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug(f"Applying 'ResizeFilter' with a factor of {self.resize_ratio}...")
        working_image = image.copy()
        width = int(image.shape[1] * self.resize_ratio)
        height = int(image.shape[0] * self.resize_ratio)
        dimensions = (width, height)
        return cv2.resize(working_image, dimensions, interpolation=cv2.INTER_AREA)
