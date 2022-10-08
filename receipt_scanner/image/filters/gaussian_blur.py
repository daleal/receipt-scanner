from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class GaussianBlurFilter(Filter):
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'GaussianBlurFilter'...")
        blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
        debug_show(blurred_image, debug=self.debug)
        return blurred_image
