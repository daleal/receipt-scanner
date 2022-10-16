from logging import getLogger

import cv2
import numpy as np

from receipt_scanner.image.filters.base_filter import Filter

logger = getLogger(__name__)


class CompressFilter(Filter):
    def eval(self, image: np.ndarray) -> np.ndarray:
        logger.debug("Applying 'CompressFilter' with automatic ratio...")
        _, encoded_image = cv2.imencode(".jpg", image)
        return cv2.imdecode(encoded_image, 1)
