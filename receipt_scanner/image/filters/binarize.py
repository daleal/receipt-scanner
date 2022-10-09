from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class BinarizeFilter(Filter):
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'BinarizeFilter'...")
        _, binarized_image = cv2.threshold(image, 168, 255, cv2.THRESH_BINARY)
        debug_show(binarized_image, debug=self.debug)
        return binarized_image
