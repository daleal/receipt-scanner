import argparse

from receipt_scanner.debug import configure_logger
from receipt_scanner.image import process_image
from receipt_scanner.image_to_text import get_text
from receipt_scanner.parser import get_items_from_text


def dispatcher():
    arguments = get_arguments()
    configure_logger(debug=arguments.debug)
    image = process_image(arguments.image, debug=arguments.debug)
    text = get_text(image)
    items = get_items_from_text(text)
    print("\n".join(items))


def get_arguments():
    parser = generate_parser()
    return parser.parse_args()


def generate_parser():
    parser = argparse.ArgumentParser()

    # Image
    parser.add_argument(
        "-i",
        "--image",
        dest="image",
        help="Path to the receipt image.",
    )

    # Debug mode
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_const",
        default=False,
        const=True,
        help="Run in debug mode.",
    )

    return parser
