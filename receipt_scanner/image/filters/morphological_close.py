from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class MorphologicalCloseFilter(Filter):
    def __init__(self, iterations: int = 3, debug: bool = False) -> None:
        self.iterations = iterations
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug(
            f"Applying 'MorphologicalCloseFilter' with {self.iterations} iterations..."
        )
        kernel = np.ones((3, 3), np.uint8)
        closed_image = cv2.morphologyEx(
            image,
            cv2.MORPH_CLOSE,
            kernel,
            iterations=self.iterations,
        )
        debug_show(closed_image, debug=self.debug)
        return closed_image
