from logging import getLogger

import cv2
import numpy as np

from .contour import find_contour
from .debug import debug_show, visualize_contour_on_image
from .filters import (
    BinarizeFilter,
    CannyFilter,
    DenoiseFilter,
    DilateFilter,
    Filter,
    GaussianBlurFilter,
    GrayscaleFilter,
    PerspectiveWrapperFilter,
    ResizeFilter,
    ThresholdsFilter,
)

logger = getLogger(__name__)


def process_image(file_name: str, debug: bool = False) -> np.ndarray:
    original_image = open_image(file_name, debug=debug)
    edge_detection_downsize_ratio = 500 / original_image.shape[0]

    downsized_image = Filter.apply(
        original_image,
        ResizeFilter(edge_detection_downsize_ratio),
    )

    processed_image = Filter.apply(
        downsized_image,
        GrayscaleFilter(debug=debug),
        GaussianBlurFilter(debug=debug),
        ThresholdsFilter(debug=debug),
        DilateFilter(debug=debug),
        CannyFilter(debug=debug),
    )

    contour = find_contour(processed_image, downsized_image, debug=debug)
    visualize_contour_on_image(downsized_image, contour, debug=debug)

    text_cleanup_downsize_ratio = 1600 / original_image.shape[0]

    return Filter.apply(
        original_image,
        PerspectiveWrapperFilter(contour, edge_detection_downsize_ratio, debug=debug),
        BinarizeFilter(debug=debug),
        DenoiseFilter(debug=debug),
        ResizeFilter(text_cleanup_downsize_ratio),
    )


def open_image(file_name: str, debug: bool = False) -> np.ndarray:
    logger.debug("Opening image...")
    original = cv2.imread(file_name)
    if original is None:
        raise Exception(f"Couldn't find file {file_name}")
    bordered_image = cv2.copyMakeBorder(original, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
    debug_show(bordered_image, debug=debug)
    return bordered_image
