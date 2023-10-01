import numpy as np
import pygame
import pretty_midi

class AudioEngine:
    def __init__(self, sample_rate=44100, duration=0.1):
        self.sample_rate = sample_rate
        self.duration = duration
        self.muted = False

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
            ["C", "D", "Eb", "F", "G", "Ab", "Bb"],  # Natural Minor
            ["C", "Db", "Eb", "E", "Gb", "Ab", "Bb"],  # Phrygian
            ["C", "D", "E", "F#", "G", "A", "B"],  # Lydian
            ["C", "D", "E", "F", "G", "A", "Bb"],  # Mixolydian
            ["C", "D", "Eb", "F", "G", "Ab", "B"],  # Harmonic minor
            ["C", "D", "E", "F", "G", "A", "Bb"],  # Dorian
            ["C", "D", "Eb", "F", "G", "Ab", "Bb"],  # Pentatonic
            ["C", "Db", "E", "F", "Gb", "Ab", "Bb"]  # Locrian
        ]
        self.scale = scales[int(zoom_level * len(scales)) % len(scales)]

        # Choose a random starting note
        note_index = np.random.choice(len(self.scale))
        base_note_name = self.scale[note_index]

        # Randomly choose an octave
        octave = np.random.choice(["3", "4", "5"])

        # Convert base note to frequency
        base_frequency = pretty_midi.note_name_to_number(base_note_name + octave)
        base_frequency = pretty_midi.note_number_to_hz(base_frequency)

        # Choose a random starting note
        note_index = np.random.choice(len(self.scale))
        self.base_note_name = self.scale[note_index]

        # Define rhythmic patterns
        rhythms = [0.25, 0.25, 0.5, 0.5, 0.5, 1]
        rhythm_factor = np.random.choice(rhythms)
        t = np.linspace(0, 2*rhythm_factor, int(self.sample_rate * rhythm_factor * 2), False)

        # Generate the tone with a lower maximum frequency for a mellow sound
        frequency = base_frequency if np.random.rand() < 0.9 else base_frequency * 2
        tone = 0.3 * np.sin(frequency * t * 2 * np.pi)

        # Generate the tone with a lower maximum frequency for a mellow sound
        frequency = base_frequency if np.random.rand() < 0.9 else base_frequency * 2
        tone = 0.3 * np.sin(frequency * t * 2 * np.pi)  # Lower amplitude also helps get a mellow sound

        # Apply an envelope to the tone to avoid harsh starts/stops
        envelope_size = int(rhythm_factor * self.sample_rate)  # Covert envelope_size to int
        envelope = np.ones_like(tone)
        envelope[:envelope_size] = np.linspace(0, 1, envelope_size)
        envelope[-envelope_size:] = np.linspace(1, 0, envelope_size)



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
            note_index = (note_index + step) % len(self.scale)  # Move to the next note in the scale
            next_note_name = self.scale[note_index]
            next_frequency = pretty_midi.note_name_to_number(next_note_name + octave)
            next_frequency = pretty_midi.note_number_to_hz(next_frequency)
            next_tone = np.sin(next_frequency * t * 2 * np.pi)
            tone_with_envelope = np.concatenate([tone_with_envelope, next_tone])


        # # Generate the chord frequencies
        # chord_frequencies = self.generate_chord(base_frequency, octave)

        # # Generate the tone for each frequency in the chord and sum them
        # tone = sum([np.sin(freq * t * 2 * np.pi) for freq in chord_frequencies[:2]])
        # # Apply an envelope to the tone to avoid harsh starts/stops
        # envelope = np.ones_like(tone)
        # envelope[:100] = np.linspace(0, 1, 100)
        # envelope[-100:] = np.linspace(1, 0, 100)
        # chord_tone_with_envelope = tone * envelope

        # # Generate melodic pattern and repeat the process
        # pattern_frequencies = self.generate_melodic_pattern(octave)[:3]
        # pattern_tone_with_envelope = sum([np.sin(freq * t * 2 * np.pi) for freq in pattern_frequencies])

        # Either generate a chord tone or a melodic pattern with 50% chance each
        coin_toss = np.random.rand()
        tone_with_envelope = tone * envelope
        if coin_toss < 0.5:  # Generate chord
            chord_frequencies = self.generate_chord(base_frequency, octave)
            chords = sum([np.sin(freq * t * 2 * np.pi) for freq in chord_frequencies])
            tone_with_envelope = np.concatenate([tone_with_envelope, chords])
        else:  # Generate melodic pattern
            if np.random.rand() < 0.25:  # Only generate a melodic pattern 25% of the time
                pattern_frequencies = self.generate_melodic_pattern(octave, length=np.random.choice([1, 2]))  # 1 or 2 note patterns
                patterns = sum([np.sin(freq * t * 2 * np.pi) for freq in pattern_frequencies])
                tone_with_envelope = np.concatenate([tone_with_envelope, patterns])

        tone_with_envelope = tone * envelope

        return tone_with_envelope

    def generate_chord(self, note_frequency, octave):
        # Find the index of base note in the scale
        base_note_index = self.scale.index(self.base_note_name)
        # Generate the triad: first, third and fifth notes in the scale
        triad_indices = [(base_note_index + i) % len(self.scale) for i in [0, 2]]
        # Convert note names to frequencies
        chord_frequencies = [pretty_midi.note_name_to_number(self.scale[i] + str(octave)) for i in triad_indices]
        chord_frequencies = [pretty_midi.note_number_to_hz(freq) for freq in chord_frequencies]
        return chord_frequencies

    def generate_melodic_pattern(self, octave, length=4):
        # Start from base note
        start_index = self.scale.index(self.base_note_name)
        # Create a sequence of "length" notes climbing the scale from the base note
        pattern_indices = [(start_index + i) % len(self.scale) for i in range(length)]
        # Convert note names to frequencies
        pattern_frequencies = [pretty_midi.note_name_to_number(self.scale[i] + str(octave)) for i in pattern_indices]
        pattern_frequencies = [pretty_midi.note_number_to_hz(freq) for freq in pattern_frequencies]
        return pattern_frequencies

    def play_sound(self, sound_array):
        if self.muted:
            return

        """Play a sound from a numpy array."""
        # Convert mono sound to stereo
        stereo_sound = np.vstack([sound_array, sound_array]).T
        # Ensure the array is C-contiguous
        contiguous_array = np.ascontiguousarray(stereo_sound)
        sound = pygame.sndarray.make_sound(np.int16(contiguous_array * 32767))
        sound.play()


    def mute(self):
        self.muted = True

    def unmute(self):
        self.muted = False
