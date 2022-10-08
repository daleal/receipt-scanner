from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class BinarizeFilter(Filter):
    def __init__(self, sigma: float = 0.33, debug: bool = False) -> None:
        self.sigma = sigma
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'BinarizeFilter'...")
        median = np.median(image)
        lower = int(max(0, (1.0 - self.sigma) * median))
        upper = int(min(255, (1.0 + self.sigma) * median))
        _, binarized_image = cv2.threshold(image, lower, upper, cv2.THRESH_BINARY)
        debug_show(binarized_image, debug=self.debug)
        return binarized_image
