import cv2
import numpy as np


def debug_show(image: np.ndarray, title: str = "Image", debug: bool = False) -> None:
    if debug:
        cv2.imshow(title, image)
        cv2.waitKey(0)


def visualize_contour_on_image(
    image: np.ndarray, contour: np.ndarray, debug: bool = False
) -> None:
    if debug:
        image_with_contour = cv2.drawContours(
            image.copy(), [contour], -1, (0, 255, 0), 2
        )
        debug_show(image_with_contour, debug=debug)
