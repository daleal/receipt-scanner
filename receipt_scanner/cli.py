import argparse
import re
from typing import TypedDict

import receipt_scanner
from receipt_scanner.core import scan


class Arguments(TypedDict):
    image_location: str
    regular_expression: re.Pattern | None
    debug: bool


def dispatcher() -> None:
    parser = generate_parser()
    arguments = process_parser(parser)
    scanned_lines = scan(**arguments)
    if arguments["debug"]:
        print("\n")
    print("Scanned text:\n===============================")
    print("\n".join(scanned_lines))


def generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    # Image
    parser.add_argument(
        "-i",
        "--image",
        dest="image_location",
        help="Location of the receipt image (can be a local path or a URL).",
    )

    # Regular Expression
    parser.add_argument(
        "-e",
        "--expression",
        dest="regular_expression",
        help="Regular Expression being used to filter the parsed text lines.",
    )

    # Debug mode
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_const",
        default=False,
        const=True,
        help="Run in debug mode.",
    )

    # Version
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"receipt-scanner version {receipt_scanner.__version__}",
    )

    return parser


def process_parser(parser: argparse.ArgumentParser) -> Arguments:
    arguments_namespace = parser.parse_args()
    return {
        "image_location": arguments_namespace.image_location,
        "regular_expression": (
            re.compile(arguments_namespace.regular_expression)
            if arguments_namespace.regular_expression
            else None
        ),
        "debug": arguments_namespace.debug,
    }
