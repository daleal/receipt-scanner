import re

from receipt_scanner.debug import configure_logger
from receipt_scanner.image import process_image
from receipt_scanner.image_to_text import get_text
from receipt_scanner.parser import filter_text


def scan(
    image_location: str,
    regular_expression: re.Pattern | None = None,
    debug: bool = False,
) -> list[str]:
    configure_logger(debug=debug)
    image = process_image(image_location, debug=debug)
    text = get_text(image)
    return filter_text(text, regular_expression)
