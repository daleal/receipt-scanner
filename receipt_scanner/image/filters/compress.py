from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.debug import debug_show
from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class CompressFilter(Filter):
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'CompressFilter' with automatic ratio...")
        _, encoded_image = cv2.imencode(".jpg", image)
        compressed_image = cv2.imdecode(encoded_image, 1)
        debug_show(compressed_image, debug=self.debug)
        return compressed_image
