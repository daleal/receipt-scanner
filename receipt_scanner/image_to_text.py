from logging import getLogger

import numpy as np
import pytesseract

logger = getLogger(__name__)


ALLOWED_CHARACTERS = (
    "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz1234567890\ .#+-:"
)


def get_text(image: np.ndarray) -> str:
    logger.debug("Extracting text from image...")
    options = {
        "config": (
            f"--psm 4 -c tessedit_char_whitelist={ALLOWED_CHARACTERS} " "-l spa+eng"
        ),
    }
    return pytesseract.image_to_string(image, **options)
