from logging import getLogger

import numpy as np

from receipt_scanner.image.constants import (
    EDGE_DETECTION_TARGET_WIDTH,
    TEXT_CLEANUP_TARGET_WIDTH,
)
from receipt_scanner.image.contour import find_contour
from receipt_scanner.image.debug import visualize_contour_on_image
from receipt_scanner.image.filters import (
    BinarizeFilter,
    CannyFilter,
    CompressFilter,
    DenoiseFilter,
    DilateFilter,
    Filter,
    GaussianBlurFilter,
    GrayscaleFilter,
    MedianBlurFilter,
    MorphologicalCloseFilter,
    PerspectiveWrapperFilter,
    ResizeFilter,
)
from receipt_scanner.image.utils import get_ratio_for_width, open_image

logger = getLogger(__name__)


def process_image(file_name: str, debug: bool = False) -> np.ndarray:
    original_image = open_image(file_name, debug=debug)
    edge_detection_resize_ratio = get_ratio_for_width(
        original_image, EDGE_DETECTION_TARGET_WIDTH
    )

    downsized_image = Filter.apply(
        original_image,
        CompressFilter(),
        ResizeFilter(edge_detection_resize_ratio),
    )

    processed_image = Filter.apply(
        downsized_image,
        MorphologicalCloseFilter(iterations=4, debug=debug),
        MedianBlurFilter(debug=debug),
        GaussianBlurFilter(size=3, debug=debug),
        CannyFilter(debug=debug),
        DilateFilter(debug=debug),
    )

    contour = find_contour(processed_image, downsized_image, debug=debug)
    visualize_contour_on_image(downsized_image, contour, debug=debug)

    wrapped_perspective_image = Filter.apply(
        original_image,
        PerspectiveWrapperFilter(contour, edge_detection_resize_ratio, debug=debug),
    )

    text_cleanup_resize_ratio = get_ratio_for_width(
        wrapped_perspective_image, TEXT_CLEANUP_TARGET_WIDTH
    )

    return Filter.apply(
        wrapped_perspective_image,
        ResizeFilter(text_cleanup_resize_ratio),
        MedianBlurFilter(debug=debug),
        DenoiseFilter(debug=debug),
        GaussianBlurFilter(debug=debug),
        GrayscaleFilter(debug=debug),
        BinarizeFilter(debug=debug),
    )
