from logging import getLogger

import numpy as np
import pytesseract

logger = getLogger(__name__)


DEFAULT_ALLOWED_CHARACTERS = (
    "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz1234567890\ ,.$/|-"
)


def get_text(image: np.ndarray, allowed_characters: str | None) -> str:
    logger.debug("Extracting text from image...")
    charset = allowed_characters or DEFAULT_ALLOWED_CHARACTERS
    options = {
        "config": f"--psm 4 -c tessedit_char_whitelist={charset} -l spa+eng",
    }
    return pytesseract.image_to_string(image, **options)
