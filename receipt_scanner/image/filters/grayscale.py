from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class GrayscaleFilter(Filter):
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'GrayscaleFilter'...")
        grayscaled_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        debug_show(grayscaled_image, debug=self.debug)
        return grayscaled_image
