"""CLI entry point for the Fractal Music Generator.

Generates MIDI music and visualizations from Mandelbrot set fractals.
"""

import argparse
import sys

from fractals import mandelbrot
from music import generate_melody, create_midi
from visualization import visualize_fractal


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate music from Mandelbrot set fractals"
    )
    parser.add_argument(
        "--max-iter", type=int, default=100,
        help="Maximum Mandelbrot iterations (default: 100)"
    )
    parser.add_argument(
        "--resolution", type=int, default=200,
        help="Fractal grid resolution (default: 200)"
    )
    parser.add_argument(
        "--base-note", type=int, default=60,
        help="Base MIDI note number, 60 = Middle C (default: 60)"
    )
    parser.add_argument(
        "--duration", type=float, default=0.25,
        help="Note duration in beats (default: 0.25)"
    )
    parser.add_argument(
        "--midi-output", type=str, default="fractal_melody.mid",
        help="Output MIDI file path (default: fractal_melody.mid)"
    )
    parser.add_argument(
        "--image-output", type=str, default="fractal_visualization.png",
        help="Output image file path (default: fractal_visualization.png)"
    )
    parser.add_argument(
        "--no-image", action="store_true",
        help="Skip generating the visualization image"
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Run the fractal music generator."""
    args = parse_args(argv)

    if args.resolution <= 0:
        print("Error: resolution must be positive", file=sys.stderr)
        sys.exit(1)
    if args.max_iter <= 0:
        print("Error: max-iter must be positive", file=sys.stderr)
        sys.exit(1)
    if not (0 <= args.base_note <= 127):
        print("Error: base-note must be in MIDI range 0-127", file=sys.stderr)
        sys.exit(1)

    print(f"Generating fractal melody (resolution={args.resolution}, "
          f"max_iter={args.max_iter})...")

    melody, timing, fractal = generate_melody(
        resolution=args.resolution,
        max_iter=args.max_iter,
        base_note=args.base_note,
        duration=args.duration,
    )

    create_midi(melody, timing, duration=args.duration, filename=args.midi_output)
    print(f"MIDI file written to: {args.midi_output}")

    if not args.no_image:
        visualize_fractal(fractal, filename=args.image_output)
        print(f"Visualization written to: {args.image_output}")

    print("Done!")


if __name__ == "__main__":
    main()
