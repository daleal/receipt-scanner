import argparse


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


def get_arguments():
    parser = generate_parser()
    return parser.parse_args()
