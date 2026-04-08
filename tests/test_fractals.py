"""Tests for fractal generation functions."""

import sys
from pathlib import Path
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from fractals import mandelbrot


class TestMandelbrot:
    """Tests for the mandelbrot() function."""

    def test_output_shape(self):
        """Output array should match requested dimensions."""
        result = mandelbrot(50, 60, max_iter=10)
        assert result.shape == (50, 60)

    def test_output_dtype(self):
        """Output should be integer iteration counts."""
        result = mandelbrot(20, 20, max_iter=10)
        assert result.dtype == int

    def test_values_in_range(self):
        """All values should be between 0 and max_iter."""
        max_iter = 25
        result = mandelbrot(30, 30, max_iter=max_iter)
        assert result.min() >= 0
        assert result.max() <= max_iter

    def test_center_point_does_not_diverge(self):
        """The origin (c=0) is in the Mandelbrot set, so it should reach max_iter."""
        max_iter = 50
        result = mandelbrot(
            100, 100, max_iter=max_iter,
            y_min=-0.01, y_max=0.01,
            x_min=-0.01, x_max=0.01,
        )
        # Center pixels should be at max_iter (part of the set)
        center = result[50, 50]
        assert center == max_iter

    def test_far_point_diverges_quickly(self):
        """Points far from the set should diverge in few iterations."""
        max_iter = 100
        result = mandelbrot(
            10, 10, max_iter=max_iter,
            y_min=10.0, y_max=10.1,
            x_min=10.0, x_max=10.1,
        )
        # All points should diverge quickly
        assert result.max() < 5

    def test_invalid_resolution_raises(self):
        """Zero or negative resolution should raise ValueError."""
        with pytest.raises(ValueError):
            mandelbrot(0, 10, max_iter=10)
        with pytest.raises(ValueError):
            mandelbrot(10, -1, max_iter=10)

    def test_invalid_max_iter_raises(self):
        """Zero or negative max_iter should raise ValueError."""
        with pytest.raises(ValueError):
            mandelbrot(10, 10, max_iter=0)

    def test_custom_bounds(self):
        """Custom complex plane bounds should work without error."""
        result = mandelbrot(20, 20, max_iter=10,
                            y_min=-2.0, y_max=2.0,
                            x_min=-2.5, x_max=1.0)
        assert result.shape == (20, 20)
