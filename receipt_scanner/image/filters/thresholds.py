from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class ThresholdsFilter(Filter):
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'ThresholdsFilter' using Binary and ToZero filters...")
        _, thresholded_image = cv2.threshold(
            image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_TOZERO
        )
        debug_show(thresholded_image, debug=self.debug)
        return thresholded_image
