from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class DilateFilter(Filter):
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'DilateFilter'...")
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilated_image = cv2.dilate(image, rect_kernel)
        debug_show(dilated_image, debug=self.debug)
        return dilated_image
