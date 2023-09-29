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

        note_index = int(zoom_level * len(scale)) % len(scale)
        base_note_name = scale[note_index]

        # Convert base note to frequency
        base_frequency = pretty_midi.note_name_to_number(base_note_name + "4")
        base_frequency = pretty_midi.note_number_to_hz(base_frequency)

        # Rhythm based on zoom level
        rhythm_factor = zoom_level % 0.5 + 0.5
        t = np.linspace(0, rhythm_factor, int(self.sample_rate * rhythm_factor), False)

        # Harmonies
        harmonies = [base_frequency]
        if zoom_level % 3 < 1:  # Add a fifth
            fifth_note = scale[(note_index + 4) % len(scale)]
            fifth_frequency = pretty_midi.note_name_to_number(fifth_note + "4")
            harmonies.append(pretty_midi.note_number_to_hz(fifth_frequency))
        elif zoom_level % 3 < 2:  # Add a third
            third_note = scale[(note_index + 2) % len(scale)]
            third_frequency = pretty_midi.note_name_to_number(third_note + "4")
            harmonies.append(pretty_midi.note_number_to_hz(third_frequency))

        # Generate the tone with harmonies
        tone = sum([np.sin(f * t * 2 * np.pi) for f in harmonies])

        # Apply a simple envelope to the tone to avoid harsh starts/stops
        envelope = np.ones_like(tone)
        envelope[:50] = np.linspace(0, 1, 50)
        envelope[-50:] = np.linspace(1, 0, 50)
        tone_with_envelope = tone * envelope

        return tone_with_envelope


    def play_sound(self, sound_array):
        """Play a sound from a numpy array."""
        # Convert mono sound to stereo
        stereo_sound = np.vstack([sound_array, sound_array]).T
        # Ensure the array is C-contiguous
        contiguous_array = np.ascontiguousarray(stereo_sound)
        sound = pygame.sndarray.make_sound(np.int16(contiguous_array * 32767))
        sound.play()

