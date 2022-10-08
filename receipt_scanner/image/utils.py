from logging import getLogger

import cv2
import numpy as np

from .debug import debug_show

logger = getLogger(__name__)


def open_image(file_name: str, debug: bool = False) -> np.ndarray:
    logger.debug("Opening image...")
    original = cv2.imread(file_name)
    if original is None:
        raise Exception(f"Couldn't find file {file_name}")
    bordered_image = cv2.copyMakeBorder(original, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
    debug_show(bordered_image, debug=debug)
    return bordered_image


def get_ratio_for_width(image: np.ndarray, target_width: int) -> float:
    image_width = image.shape[1]
    return target_width / image_width
