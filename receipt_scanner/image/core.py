from logging import getLogger

import cv2
import numpy as np

from .debug import debug_show, visualize_contour_on_image
from .utils import approximate_contour, contour_to_rect, wrap_perspective

logger = getLogger(__name__)


def process_image(file_name: str, debug: bool = False) -> np.ndarray:
    original_image = open_image(file_name, debug=debug)
    downsize_ratio = 500 / original_image.shape[0]
    downsized_image = resize_image(original_image, downsize_ratio)
    grayscaled_image = convert_to_grayscale(downsized_image, debug=debug)
    blurred_image = apply_gaussian_blur(grayscaled_image, debug=debug)
    thresholded_image = apply_thresholds(blurred_image, debug=debug)
    white_regions_detected_image = detect_white_regions(thresholded_image, debug=debug)
    edged_image = detect_edges(white_regions_detected_image, debug=debug)
    contours = detect_contours(edged_image, downsized_image)
    largest_contours = filter_largest_contours(contours, downsized_image, debug=debug)
    best_contour = find_best_rectangular_contour(largest_contours)
    contour = approximate_contour(best_contour)
    visualize_contour_on_image(downsized_image, contour, debug=debug)
    wrapped_perspective_image = wrap_image_perspective(
        original_image, contour, downsize_ratio, debug=debug
    )
    binarized_image = binarize_image(wrapped_perspective_image, debug=debug)
    denoised_image = denoise_image(binarized_image, debug=debug)
    downsize_ratio = 1600 / denoised_image.shape[0]
    return resize_image(denoised_image, downsize_ratio)


def open_image(file_name: str, debug: bool = False) -> np.ndarray:
    logger.debug("Opening image...")
    original = cv2.imread(file_name)
    if original is None:
        raise Exception(f"Couldn't find file {file_name}")
    bordered_image = cv2.copyMakeBorder(original, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
    debug_show(bordered_image, debug=debug)
    return bordered_image


def resize_image(image: np.ndarray, resize_ratio: float) -> np.ndarray:
    logger.debug(f"Resizing image using a factor of {resize_ratio}...")
    working_image = image.copy()
    width = int(image.shape[1] * resize_ratio)
    height = int(image.shape[0] * resize_ratio)
    dimensions = (width, height)
    return cv2.resize(working_image, dimensions, interpolation=cv2.INTER_AREA)


def convert_to_grayscale(image: np.ndarray, debug: bool = False) -> np.ndarray:
    logger.debug("Converting to grayscale...")
    grayscaled_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    debug_show(grayscaled_image, debug=debug)
    return grayscaled_image


def apply_gaussian_blur(image: np.ndarray, debug: bool = False) -> np.ndarray:
    logger.debug("Applying Gaussian blur...")
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    debug_show(blurred_image, debug=debug)
    return blurred_image


def apply_thresholds(image: np.ndarray, debug: bool = False) -> np.ndarray:
    logger.debug("Applying Binary and ToZero thresholds...")
    _, thresholded_image = cv2.threshold(
        image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_TOZERO
    )
    debug_show(thresholded_image, debug=debug)
    return thresholded_image


def detect_white_regions(image: np.ndarray, debug: bool = False) -> np.ndarray:
    logger.debug("Detecting white regions...")
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    white_regions_detected_image = cv2.dilate(image, rect_kernel)
    debug_show(white_regions_detected_image, debug=debug)
    return white_regions_detected_image


def detect_edges(
    image: np.ndarray, sigma: float = 0.33, debug: bool = False
) -> np.ndarray:
    logger.debug("Detecting edges...")
    median = np.median(image)
    lower = int(max(0, (1.0 - sigma) * median))
    upper = int(min(255, (1.0 + sigma) * median))
    edges_detected_image = cv2.Canny(image, lower, upper)
    debug_show(edges_detected_image, debug=debug)
    return edges_detected_image


def detect_contours(
    edged_image: np.ndarray, original_image: np.ndarray, debug: bool = False
) -> list[np.ndarray]:
    logger.debug("Detecting contours...")
    contours, _ = cv2.findContours(edged_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_detected_image = cv2.drawContours(
        original_image.copy(), contours, -1, (0, 255, 0), 3
    )
    debug_show(contours_detected_image, debug=debug)
    return list(contours)


def filter_largest_contours(
    contours: list[np.ndarray],
    original_image: np.ndarray,
    amount: int = 3,
    debug: bool = False,
) -> list[np.ndarray]:
    logger.debug("Filtering smaller contours...")
    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:amount]
    image_with_largest_contours = cv2.drawContours(
        original_image.copy(), largest_contours, -1, (0, 255, 0), 3
    )
    debug_show(image_with_largest_contours, debug=debug)
    return largest_contours


def find_best_rectangular_contour(contours: list[np.ndarray]):
    logger.debug("Searching for the best contour...")
    for contour in contours:
        contour_approximation = approximate_contour(contour)
        if len(contour_approximation) == 4:
            return contour_approximation
    raise Exception("No valid contour was found")


def wrap_image_perspective(
    image: np.ndarray, contour: np.ndarray, resize_ratio: float, debug: bool = False
) -> np.ndarray:
    logger.debug("Wrapping image perspective...")
    working_image = image.copy()
    contour_rect = contour_to_rect(contour, resize_ratio)
    wrapped_perspective_image = wrap_perspective(working_image, contour_rect)
    debug_show(wrapped_perspective_image, debug=debug)
    return wrapped_perspective_image


def binarize_image(
    image: np.ndarray, sigma: float = 0.33, debug: bool = False
) -> np.ndarray:
    logger.debug("Binarizing image...")
    median = np.median(image)
    lower = int(max(0, (1.0 - sigma) * median))
    upper = int(min(255, (1.0 + sigma) * median))
    _, binarized_image = cv2.threshold(image, lower, upper, cv2.THRESH_BINARY)
    debug_show(binarized_image, debug=debug)
    return binarized_image


def denoise_image(image: np.ndarray, debug: bool = False) -> np.ndarray:
    logger.debug("Denoising image...")
    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    debug_show(denoised_image, debug=debug)
    return denoised_image
