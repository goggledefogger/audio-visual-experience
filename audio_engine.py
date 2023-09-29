import numpy as np
import pygame
import pretty_midi

class AudioEngine:
    def __init__(self, sample_rate=44100, duration=0.1):
        self.sample_rate = sample_rate
        self.duration = duration

    def note_to_frequency(self, note_name):
        """Convert a note name (e.g., 'C4') to its frequency in Hz."""
        midi_note = pretty_midi.note_name_to_number(note_name)
        frequency = pretty_midi.note_number_to_hz(midi_note)
        return frequency

    def generate_tone_with_envelope(self, zoom_level):
        """Generate a tone based on the zoom level and apply an envelope."""
        # Scales and modes for variation
        scales = [
            ["C", "D", "E", "F", "G", "A", "B"],  # Major
            ["C", "D", "Eb", "F", "G", "Ab", "Bb"],  # Minor
            ["C", "D", "E", "G", "A"],  # Pentatonic
            ["C", "D", "Eb", "F", "G", "A", "Bb"],  # Dorian
        ]
        scale = scales[int(zoom_level * len(scales)) % len(scales)]

        # Choose a random starting note
        note_index = np.random.choice(len(scale))
        base_note_name = scale[note_index]

        # Randomly choose an octave
        octave = np.random.choice(["3", "4", "5"])

        # Convert base note to frequency
        base_frequency = pretty_midi.note_name_to_number(base_note_name + octave)
        base_frequency = pretty_midi.note_number_to_hz(base_frequency)

        # Define rhythmic patterns
        rhythms = [0.25, 0.5, 0.125, 0.375, 0.75]  # Quarter, half, eighth, dotted-eighth, etc.
        rhythm_factor = np.random.choice(rhythms)
        t = np.linspace(0, rhythm_factor, int(self.sample_rate * rhythm_factor), False)

        # Generate the tone
        tone = np.sin(base_frequency * t * 2 * np.pi)

        # Reduce amplitude to limit distortion
        tone = 0.5 * tone

        # Apply an envelope to the tone to avoid harsh starts/stops
        envelope = np.ones_like(tone)
        envelope[:100] = np.linspace(0, 1, 100)
        envelope[-100:] = np.linspace(1, 0, 100)
        tone_with_envelope = tone * envelope

        # Add melodic patterns (arpeggios, leaps, and steps)
        if np.random.rand() < 0.5:  # 50% chance to add a melodic pattern
            step = np.random.choice([-2, -1, 1, 2])  # Choose a step size (up or down)
            note_index = (note_index + step) % len(scale)  # Move to the next note in the scale
            next_note_name = scale[note_index]
            next_frequency = pretty_midi.note_name_to_number(next_note_name + octave)
            next_frequency = pretty_midi.note_number_to_hz(next_frequency)
            next_tone = np.sin(next_frequency * t * 2 * np.pi)
            tone_with_envelope = np.concatenate([tone_with_envelope, next_tone])

        return tone_with_envelope


    def play_sound(self, sound_array):
        """Play a sound from a numpy array."""
        # Convert mono sound to stereo
        stereo_sound = np.vstack([sound_array, sound_array]).T
        # Ensure the array is C-contiguous
        contiguous_array = np.ascontiguousarray(stereo_sound)
        sound = pygame.sndarray.make_sound(np.int16(contiguous_array * 32767))
        sound.play()

