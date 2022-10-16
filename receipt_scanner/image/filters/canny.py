from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class CannyFilter(Filter):
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'CannyFilter'...")
        edges_detected_image = cv2.Canny(image, 0, 200)
        debug_show(edges_detected_image, debug=self.debug)
        return edges_detected_image
