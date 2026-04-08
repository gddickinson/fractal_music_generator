"""Tests for MIDI music generation."""

import sys
import os
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from music import generate_melody, create_midi


class TestGenerateMelody:
    """Tests for generate_melody()."""

    def test_returns_three_elements(self):
        """Should return (melody, timing, fractal) tuple."""
        melody, timing, fractal = generate_melody(
            resolution=20, max_iter=10, base_note=60, duration=0.25
        )
        assert isinstance(melody, list)
        assert isinstance(timing, list)
        assert len(melody) == len(timing)

    def test_melody_notes_in_midi_range(self):
        """All notes should be valid MIDI values."""
        melody, _, _ = generate_melody(
            resolution=20, max_iter=10, base_note=60
        )
        for note in melody:
            assert 0 <= note <= 127

    def test_timing_is_monotonic(self):
        """Timing values should be non-decreasing."""
        _, timing, _ = generate_melody(
            resolution=20, max_iter=10
        )
        for i in range(1, len(timing)):
            assert timing[i] >= timing[i - 1]

    def test_invalid_base_note_raises(self):
        """base_note outside 0-127 should raise ValueError."""
        with pytest.raises(ValueError):
            generate_melody(resolution=20, max_iter=10, base_note=200)

    def test_invalid_duration_raises(self):
        """Non-positive duration should raise ValueError."""
        with pytest.raises(ValueError):
            generate_melody(resolution=20, max_iter=10, duration=-1)


class TestCreateMidi:
    """Tests for create_midi()."""

    def test_creates_file(self):
        """Should create a MIDI file on disk."""
        melody = [60, 62, 64, 65, 67]
        timing = [0.0, 0.25, 0.5, 0.75, 1.0]
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
            path = f.name
        try:
            create_midi(melody, timing, duration=0.25, filename=path)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_empty_melody(self):
        """Empty melody should still produce a valid file."""
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
            path = f.name
        try:
            create_midi([], [], duration=0.25, filename=path)
            assert os.path.exists(path)
        finally:
            os.unlink(path)
