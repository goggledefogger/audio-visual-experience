import pygame
import numpy as np
import mingus.core.notes as notes
import pretty_midi


class AudioEngine:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        pygame.mixer.init(frequency=sample_rate, size=-16, channels=2, buffer=1024)
        pygame.mixer.set_num_channels(8)
        self.scale = ["C", "D", "E", "F", "G", "A", "B"]

    def note_to_frequency(self, note_name):
        """Convert a musical note name to its frequency."""
        midi_note = pretty_midi.note_name_to_number(note_name)
        return pretty_midi.note_number_to_hz(midi_note)

    def generate_tone_with_envelope(self, zoom_factor, volume=0.2, duration=0.1):
        note_index = int((1.0 / zoom_factor) % len(self.scale))
        note_name = self.scale[note_index]
        frequency = self.note_to_frequency(note_name + "4")  # Using the 4th octave

        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        tone = np.sin(2 * np.pi * frequency * t)

        fade_time = int(self.sample_rate * duration * 0.1)
        envelope = np.concatenate([np.linspace(0, 1, fade_time),
                                   np.ones(len(t) - 2 * fade_time),
                                   np.linspace(1, 0, fade_time)])
        tone *= envelope

        stereo_tone = np.vstack([tone, tone]).T
        contiguous_array = np.ascontiguousarray(np.int16(stereo_tone * volume * 32767))
        sound = pygame.sndarray.make_sound(contiguous_array)
        return sound
