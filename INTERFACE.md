# Fractal Music Generator -- Interface Map

## Project Structure

### Entry Point
- **main.py** -- CLI entry point with argparse (--max-iter, --resolution, --base-note, --duration, --midi-output, --image-output, --no-image)

### Modules
- **fractals.py** -- `mandelbrot(h, w, max_iter, ...)` -- Mandelbrot set computation with configurable complex plane bounds
- **music.py** -- `generate_melody(resolution, max_iter, ...)` -- Maps fractal data to MIDI notes; `create_midi(melody, timing, ...)` -- Writes MIDI file
- **visualization.py** -- `visualize_fractal(fractal, filename)` -- Renders fractal as colored PNG

### Legacy
- **fractal-music.py** -- Original single-file version (kept for reference)
- **fractal_music.py** -- Importable copy of original (kept for backward compat)

### Tests (`tests/`)
- **test_fractals.py** -- Tests for mandelbrot(): shape, dtype, ranges, bounds, validation
- **test_music.py** -- Tests for generate_melody() and create_midi(): MIDI range, timing, file creation
