"""Module dedicated to extraction of Statistical Metafeatures.

Todo:
    * Implement metafeatures.
    * Improve documentation.
"""
import typing as t

import numpy as np


class MFEStatistical:
    """To do this documentation."""

    @classmethod
    def ft_mean(cls, N: np.ndarray) -> t.Union[np.ndarray, float]:
        """Returns the mean value of each data column."""
        return N.mean(axis=0)