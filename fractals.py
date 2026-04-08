"""Fractal generation functions.

Provides Mandelbrot set computation with configurable parameters.
"""

import numpy as np


def mandelbrot(h: int, w: int, max_iter: int,
               y_min: float = -1.4, y_max: float = 1.4,
               x_min: float = -2.0, x_max: float = 0.8) -> np.ndarray:
    """Compute the Mandelbrot set divergence times.

    Args:
        h: Height (number of rows) of the output array.
        w: Width (number of columns) of the output array.
        max_iter: Maximum number of iterations before considering a point
            as part of the set.
        y_min: Minimum imaginary component of the complex plane bounds.
        y_max: Maximum imaginary component of the complex plane bounds.
        x_min: Minimum real component of the complex plane bounds.
        x_max: Maximum real component of the complex plane bounds.

    Returns:
        2D numpy array of divergence iteration counts.
    """
    if h <= 0 or w <= 0:
        raise ValueError("Resolution dimensions must be positive")
    if max_iter <= 0:
        raise ValueError("max_iter must be positive")

    y, x = np.ogrid[y_min:y_max:h * 1j, x_min:x_max:w * 1j]
    c = x + y * 1j
    z = c.copy()
    divtime = max_iter + np.zeros(z.shape, dtype=int)

    for i in range(max_iter):
        z = z ** 2 + c
        diverge = z * np.conj(z) > 2 ** 2
        div_now = diverge & (divtime == max_iter)
        divtime[div_now] = i
        z[diverge] = 2

    return divtime
