import numpy as np
from midiutil import MIDIFile
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.signal import savgol_filter

class FractalMusicGenerator:
    def __init__(self, max_iter=100, resolution=200):
        self.max_iter = max_iter
        self.resolution = resolution
        self.scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.base_note = 60  # Middle C
        self.duration = 0.25  # Quarter note
        
    def mandelbrot(self, h, w, max_iter):
        y, x = np.ogrid[-1.4:1.4:h*1j, -2:0.8:w*1j]
        c = x + y*1j
        z = c
        divtime = max_iter + np.zeros(z.shape, dtype=int)

        for i in range(max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2

        return divtime
    
    def generate_melody(self):
        # Generate Mandelbrot set
        fractal = self.mandelbrot(self.resolution, self.resolution, self.max_iter)
        
        # Create melody from the fractal pattern
        melody = []
        timing = []
        current_time = 0
        
        # Extract a musical path through the fractal
        for i in range(self.resolution):
            row_values = fractal[i, :]
            # Smooth the values to create more musical transitions
            smoothed = savgol_filter(row_values, 15, 3)
            # Scale to musical range
            notes = (smoothed % 12 + self.base_note).astype(int)
            
            # Add interesting notes to the melody
            for note in notes[::4]:  # Take every 4th note to reduce density
                if note % 12 in [0, 2, 4, 5, 7, 9, 11]:  # Major scale notes
                    melody.append(int(note))
                    timing.append(current_time)
                    current_time += self.duration
        
        return melody, timing, fractal
    
    def create_midi(self, filename="fractal_melody.mid"):
        melody, timing, _ = self.generate_melody()
        
        # Create MIDI file
        midi = MIDIFile(1)
        track = 0
        time = 0
        midi.addTrackName(track, time, "Fractal Melody")
        midi.addTempo(track, time, 120)
        
        # Add notes to MIDI file
        for i, (pitch, time) in enumerate(zip(melody, timing)):
            # Vary velocity (volume) based on position in sequence
            velocity = 70 + int(20 * np.sin(i/10))
            midi.addNote(track, 0, pitch, time, self.duration, velocity)
        
        # Save MIDI file
        with open(filename, "wb") as f:
            midi.writeFile(f)
            
    def visualize(self, filename="fractal_visualization.png"):
        _, _, fractal = self.generate_melody()
        
        # Create custom colormap
        colors = ['darkblue', 'blue', 'violet', 'magenta', 'orange', 'yellow']
        n_bins = 100
        cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
        
        # Plot fractal
        plt.figure(figsize=(12, 12))
        plt.imshow(fractal, cmap=cmap)
        plt.colorbar(label='Iteration count')
        plt.title('Fractal Pattern Used for Music Generation')
        plt.axis('off')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

# Create and use the generator
if __name__ == "__main__":
    generator = FractalMusicGenerator(max_iter=100, resolution=200)
    
    # Generate both MIDI and visualization
    generator.create_midi("fractal_melody.mid")
    generator.visualize("fractal_visualization.png")
    
    print("Generated fractal melody and visualization!")
    print("Please check 'fractal_melody.mid' for the music")
    print("and 'fractal_visualization.png' for the visualization.")