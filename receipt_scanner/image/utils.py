from logging import getLogger

import cv2
import httpx
import numpy as np

from receipt_scanner.image.debug import debug_show

logger = getLogger(__name__)


def open_image(image_location: str, debug: bool = False) -> np.ndarray:
    logger.debug("Opening image...")
    original = fetch_image(image_location)
    bordered_image = cv2.copyMakeBorder(original, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
    debug_show(bordered_image, debug=debug)
    return bordered_image


def get_ratio_for_width(image: np.ndarray, target_width: int) -> float:
    image_width = image.shape[1]
    return target_width / image_width


def fetch_image(image_location: str) -> np.ndarray:
    try:
        response = httpx.get(image_location)
        image_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
        image = cv2.imdecode(image_array, -1)
    except (cv2.error, httpx.UnsupportedProtocol):
        image = cv2.imread(image_location)
    if image is None:
        raise FileNotFoundError(f"Couldn't find image located at '{image_location}'")
    return image
