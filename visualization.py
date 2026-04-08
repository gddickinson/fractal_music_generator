"""Fractal visualization functions.

Renders fractal arrays as images with custom colormaps.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def visualize_fractal(fractal: np.ndarray,
                      filename: str = "fractal_visualization.png") -> None:
    """Save a fractal array as a colored PNG image.

    Args:
        fractal: 2D numpy array of iteration counts.
        filename: Output image file path.
    """
    colors = ['darkblue', 'blue', 'violet', 'magenta', 'orange', 'yellow']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

    plt.figure(figsize=(12, 12))
    plt.imshow(fractal, cmap=cmap)
    plt.colorbar(label='Iteration count')
    plt.title('Fractal Pattern Used for Music Generation')
    plt.axis('off')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
