from __future__ import annotations

from abc import ABCMeta, abstractmethod
from functools import reduce

import numpy as np


class Filter(metaclass=ABCMeta):
    @staticmethod
    def apply(
        base_image: np.ndarray,
        *filters: Filter,
    ) -> np.ndarray:
        return reduce(
            lambda base, image_filter: image_filter.eval(base),
            filters,
            base_image,
        )

    @abstractmethod
    def eval(self, image: np.ndarray) -> np.ndarray:
        ...
