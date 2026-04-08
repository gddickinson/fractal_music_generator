"""MIDI music generation from fractal data.

Maps fractal iteration counts to MIDI notes and produces .mid files.
"""

import numpy as np
from midiutil import MIDIFile
from scipy.signal import savgol_filter
from typing import Tuple, List

from fractals import mandelbrot


def generate_melody(resolution: int, max_iter: int, base_note: int = 60,
                    duration: float = 0.25) -> Tuple[List[int], List[float], np.ndarray]:
    """Generate a melody from the Mandelbrot set.

    Args:
        resolution: Grid resolution (produces resolution x resolution fractal).
        max_iter: Maximum Mandelbrot iterations.
        base_note: Base MIDI note number (default 60 = Middle C).
        duration: Note duration in beats.

    Returns:
        Tuple of (melody notes, timing list, fractal array).
    """
    if base_note < 0 or base_note > 127:
        raise ValueError("base_note must be in MIDI range 0-127")
    if duration <= 0:
        raise ValueError("duration must be positive")

    fractal = mandelbrot(resolution, resolution, max_iter)

    melody = []
    timing = []
    current_time = 0.0

    for i in range(resolution):
        row_values = fractal[i, :]
        smoothed = savgol_filter(row_values, 15, 3)
        notes = (smoothed % 12 + base_note).astype(int)

        for note in notes[::4]:
            if note % 12 in [0, 2, 4, 5, 7, 9, 11]:  # Major scale notes
                melody.append(int(note))
                timing.append(current_time)
                current_time += duration

    return melody, timing, fractal


def create_midi(melody: List[int], timing: List[float],
                duration: float = 0.25, filename: str = "fractal_melody.mid") -> None:
    """Write a melody to a MIDI file.

    Args:
        melody: List of MIDI note numbers.
        timing: List of note start times in beats.
        duration: Note duration in beats.
        filename: Output MIDI file path.
    """
    midi = MIDIFile(1)
    track = 0
    midi.addTrackName(track, 0, "Fractal Melody")
    midi.addTempo(track, 0, 120)

    for i, (pitch, time) in enumerate(zip(melody, timing)):
        velocity = 70 + int(20 * np.sin(i / 10))
        midi.addNote(track, 0, pitch, time, duration, velocity)

    with open(filename, "wb") as f:
        midi.writeFile(f)
