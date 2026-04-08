# Fractal Music Generator -- Roadmap

## Current State
A single-file project (`fractal-music.py`) containing a `FractalMusicGenerator` class that maps Mandelbrot set iteration counts to MIDI notes. Outputs `fractal_melody.mid` and `fractal_visualization.png`. Uses numpy, midiutil, matplotlib, and scipy (Savitzky-Golay filter for smoothing). Functional but minimal -- no CLI, no configuration, no tests, no package structure.

## Short-term Improvements
- [x] Rename `fractal-music.py` to `fractal_music.py` for importability
- [x] Add argparse CLI for `max_iter`, `resolution`, `base_note`, `duration`, output paths (see `main.py`)
- [x] Add `requirements.txt` (numpy, matplotlib, midiutil, scipy)
- [x] Split into modules: `fractals.py` (Mandelbrot computation), `music.py` (MIDI generation), `visualization.py` (plotting), `main.py` (CLI entry point)
- [x] Add input validation (resolution > 0, max_iter > 0, valid MIDI note range)
- [x] Add docstrings to all methods
- [x] Add `.gitignore`
- [x] Add tests: `tests/test_fractals.py` (8 tests), `tests/test_music.py` (7 tests)

## Feature Enhancements
- [ ] Add Julia set and Burning Ship fractal generators as alternative sources
- [ ] Implement scale selection (major, minor, pentatonic, blues, chromatic) via CLI flag
- [ ] Add multi-track support (harmony, bass line, drums derived from different fractal slices)
- [ ] Add rhythm variation -- map fractal values to note durations, not just pitches
- [ ] Implement real-time audio preview using `pygame.midi` or `fluidsynth`
- [ ] Add an interactive mode -- click on the fractal visualization to hear that region's melody

## Long-term Vision
- [ ] Build a GUI (PyQt or web-based) for interactive fractal exploration with live audio
- [ ] Add MIDI-to-audio rendering (SoundFont support) so output is WAV/MP3, not just MIDI
- [ ] Support custom fractal functions defined by the user (z^n + c for arbitrary n)
- [ ] Implement algorithmic harmony -- generate chord progressions from 2D fractal regions
- [ ] Publish as a pip-installable package and web demo

## Technical Debt
- [x] Everything split into separate modules with clear separation of concerns
- [x] Tests added -- the Mandelbrot computation and scale mapping are now tested
- [x] Hardcoded complex plane bounds parameterized in `fractals.py` `mandelbrot()` function
- [ ] `self.scale` stores note names but they are never used -- scale filtering uses hardcoded logic
- [ ] No error handling for midiutil failures or file write permissions
- [x] Output files use configurable paths via CLI arguments
