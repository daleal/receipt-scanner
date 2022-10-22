from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class GaussianBlurFilter(Filter):
    def __init__(self, size: int = 7, debug: bool = False) -> None:
        self.size = size
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug(f"Applying 'GaussianBlurFilter' with size {self.size}...")
        blurred_image = cv2.GaussianBlur(image, (self.size, self.size), 0)
        debug_show(blurred_image, debug=self.debug)
        return blurred_image
