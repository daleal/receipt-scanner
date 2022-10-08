from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class CannyFilter(Filter):
    def __init__(self, sigma: float = 0.33, debug: bool = False) -> None:
        self.sigma = sigma
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'CannyFilter'...")
        median = np.median(image)
        lower = int(max(0, (1.0 - self.sigma) * median))
        upper = int(min(255, (1.0 + self.sigma) * median))
        edges_detected_image = cv2.Canny(image, lower, upper)
        debug_show(edges_detected_image, debug=self.debug)
        return edges_detected_image
