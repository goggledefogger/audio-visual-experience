import numpy as np
import pygame
import pretty_midi

class AudioEngine:
    def __init__(self, sample_rate=44100, duration=0.1):
        self.sample_rate = sample_rate
        self.duration = duration
        self.muted = False
        self.mode = AudioEngine.DefaultAudioMode(self)  # Set the default mode

    def note_to_frequency(self, note_name):
        """Convert a note name (e.g., 'C4') to its frequency in Hz."""
        midi_note = pretty_midi.note_name_to_number(note_name)
        frequency = pretty_midi.note_number_to_hz(midi_note)
        return frequency

    def generate_tone_with_envelope(self, zoom_level, rotation_angle=0, color_intensity=0.5, pattern_density=0.5):
        return self.mode.generate_sound(zoom_level, rotation_angle, color_intensity, pattern_density)

    def generate_chord(self, base_frequency, octave_multiplier=1):
        """Generate a chord based on the base frequency and the current mode's scale."""
        base_note_index = self.mode.scale.index(self.mode.base_note_name)
        chord_indices = [base_note_index] + [base_note_index + i for i in self.mode.chord_intervals]
        chord_frequencies = [base_frequency * (2 ** (i / 12)) for i in chord_indices]
        return [freq * octave_multiplier for freq in chord_frequencies]

    def generate_melodic_pattern(self, octave_multiplier, length=4):
        # Start from base note
        start_index = self.mode.scale.index(self.mode.base_note_name)
        # Create a sequence of "length" notes climbing the scale from the base note
        pattern_indices = [(start_index + i) % len(self.mode.scale) for i in range(length)]
        # Convert note names to frequencies
        pattern_frequencies = [pretty_midi.note_name_to_number(self.mode.scale[i] + str(octave_multiplier)) for i in pattern_indices]
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


    # Base class for audio modes
    class BaseAudioMode:
        def __init__(self, audio_engine):
            self.audio_engine = audio_engine
            self.scales = [
                ["C", "D", "Eb", "F", "G", "Ab", "Bb"],  # Pentatonic
            ]
            self.scale = self.scales[0]
            self.base_note_name = self.scale[0]  # Default to the first note of the scale


        def generate_sound(self, zoom_level, rotation_angle, color_intensity, pattern_density):
            raise NotImplementedError("Each audio mode must implement this method.")

    # Default audio mode
    class DefaultAudioMode(BaseAudioMode):
        def __init__(self, audio_engine):
            super().__init__(audio_engine)
            self.scales = [
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
            self.scale = self.scales[0]  # Default to Major scale
            self.chord_intervals = [0, 4, 7]  # Major triad chord intervals
            self.base_note_name = "C"  # Default base note

        def generate_sound(self, zoom_level, rotation_angle, color_intensity, pattern_density):
            """Generate a tone based on the zoom level and apply an envelope."""
            self.scale = self.scales[int(zoom_level * len(self.scales)) % len(self.scales)]

            # Choose a random starting note
            note_index = np.random.choice(len(self.scale))
            base_note_name = self.scale[note_index]

            # Randomly choose an octave
            octave = np.random.choice(["3", "4", "5"])
            # Randomly choose an octave multiplier
            octave_multiplier = np.random.choice([1, 2, 4])


            # Convert base note to frequency
            base_frequency = pretty_midi.note_name_to_number(base_note_name + octave)
            base_frequency = pretty_midi.note_number_to_hz(base_frequency)

            # Choose a random starting note
            note_index = np.random.choice(len(self.scale))
            self.base_note_name = self.scale[note_index]

            # Define rhythmic patterns
            rhythms = [0.25, 0.25, 0.5, 0.5, 0.5, 1]
            rhythm_factor = np.random.choice(rhythms)
            t = np.linspace(0, 2*rhythm_factor, int(self.audio_engine.sample_rate * rhythm_factor * 2), False)

            # Generate the tone with a lower maximum frequency for a mellow sound
            frequency = base_frequency if np.random.rand() < 0.9 else base_frequency * 2
            tone = 0.3 * np.sin(frequency * t * 2 * np.pi)

            # Generate the tone with a lower maximum frequency for a mellow sound
            frequency = base_frequency if np.random.rand() < 0.9 else base_frequency * 2
            tone = 0.3 * np.sin(frequency * t * 2 * np.pi)  # Lower amplitude also helps get a mellow sound

            # Apply an envelope to the tone to avoid harsh starts/stops
            envelope_size = int(rhythm_factor * self.audio_engine.sample_rate)  # Access sample_rate through audio_engine
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
                chord_frequencies = self.audio_engine.generate_chord(base_frequency, octave_multiplier)
                chords = sum([np.sin(freq * t * 2 * np.pi) for freq in chord_frequencies])
                tone_with_envelope = np.concatenate([tone_with_envelope, chords])
            else:  # Generate melodic pattern
                if np.random.rand() < 0.25:  # Only generate a melodic pattern 25% of the time
                    pattern_frequencies = self.audio_engine.generate_melodic_pattern(octave, length=np.random.choice([1, 2]))  # 1 or 2 note patterns
                    patterns = sum([np.sin(freq * t * 2 * np.pi) for freq in pattern_frequencies])
                    tone_with_envelope = np.concatenate([tone_with_envelope, patterns])

            tone_with_envelope = tone * envelope

            return tone_with_envelope
    class PulsatingAudioMode(BaseAudioMode):
        def __init__(self, audio_engine):
            super().__init__(audio_engine)

        def generate_sound(self, zoom_level, rotation_angle, color_intensity, pattern_density):
            """Generate an enhanced pulsating tone based on various visualization factors."""

            # Dynamic base frequency based on zoom level and rotation angle
            base_frequency = 220.0 + 220.0 * zoom_level + rotation_angle  # Vary with zoom and rotation

            t = np.linspace(0, self.audio_engine.duration, int(self.audio_engine.sample_rate * self.audio_engine.duration), False)

            # Pulsation effect influenced by color intensity
            modulator_frequency = 2.0 + 10.0 * zoom_level + 5.0 * color_intensity
            pulsation_depth = 0.5 + 0.5 * zoom_level
            modulator = pulsation_depth * (1.0 + np.sin(2 * np.pi * modulator_frequency * t))

            # Base tone with harmonic overtones influenced by pattern density
            tone = np.sin(2 * np.pi * base_frequency * t)
            harmonic1 = 0.5 * pattern_density * np.sin(2 * np.pi * 2 * base_frequency * t)
            harmonic2 = 0.3 * (1 - pattern_density) * np.sin(2 * np.pi * 3 * base_frequency * t)
            combined_tone = tone + harmonic1 + harmonic2

            # Apply the pulsating effect
            pulsating_tone = combined_tone * modulator

            # Dynamic rhythmic patterns based on color intensity
            if color_intensity > 0.7:  # Introduce rhythmic breaks for high color intensities
                break_point = np.random.randint(len(t) // 2, len(t) - 100)
                pulsating_tone[break_point:break_point+100] = 0

            # Apply an envelope to the tone
            envelope = np.ones_like(pulsating_tone)
            envelope[:100] = np.linspace(0, 1, 100)
            envelope[-100:] = np.linspace(1, 0, 100)
            pulsating_tone_with_envelope = pulsating_tone * envelope

            return pulsating_tone_with_envelope

    class AmbientNeuroMode(BaseAudioMode):
        def __init__(self, audio_engine):
            super().__init__(audio_engine)

        def generate_sound(self, zoom_level, rotation_angle, color_intensity, pattern_density):
            """Generate an ambient neuro-inspired tone based on visualization factors."""

            t = np.linspace(0, self.audio_engine.duration + 1.5, int(self.audio_engine.sample_rate * (self.audio_engine.duration + 1.5)), False)

            # Base frequency influenced by zoom level and rotation angle
            base_frequency = 110.0 + 55.0 * zoom_level + rotation_angle

            # Binaural beat effect
            binaural_offset = 5.0  # 5 Hz binaural beat for relaxation
            left_ear_tone = np.sin(2 * np.pi * base_frequency * t)
            right_ear_tone = np.sin(2 * np.pi * (base_frequency + binaural_offset) * t)
            binaural_tone = (left_ear_tone + right_ear_tone) / 2.0

            # Ambient chord texture
            sus2_harmonic = np.sin(2 * np.pi * 2 * base_frequency * t)
            sus4_harmonic = np.sin(2 * np.pi * 4/3 * base_frequency * t)
            chord_texture = 0.5 * sus2_harmonic + 0.5 * sus4_harmonic

            # Random ambient textures
            random_texture = np.interp(t, np.linspace(0, self.audio_engine.duration, 10), np.random.uniform(-1, 1, 10))
            random_texture = random_texture * (0.1 + 0.2 * color_intensity)

            # Combine all elements
            combined_tone = binaural_tone + chord_texture + random_texture

            # Apply a slow attack and release envelope
            envelope = np.ones_like(combined_tone)
            envelope[:100] = np.linspace(0, 1, 100)
            envelope[-100:] = np.linspace(1, 0, 100)
            combined_tone_with_envelope = combined_tone * envelope

            # envelope = np.ones(int(self.audio_engine.sample_rate * self.audio_engine.duration))
            # attack_duration = int(0.5 * self.audio_engine.sample_rate)  # 0.5 seconds
            # release_duration = int(1 * self.audio_engine.sample_rate)  # 1 second
            # envelope[:attack_duration] = np.linspace(0, 1, attack_duration)
            # envelope[-release_duration:] = np.linspace(1, 0, release_duration)
            # ambient_neuro_tone = combined_tone * envelope

            # return ambient_neuro_tone
            # return combined_tone

            return combined_tone_with_envelope

    class EtherealAmbientMode(BaseAudioMode):
        def __init__(self, audio_engine):
            super().__init__(audio_engine)

        def generate_sound(self, zoom_level, rotation_angle, color_intensity, pattern_density):
            """Generate a multi-layered, minimalistic, and calming tone."""

            t = np.linspace(0, self.audio_engine.duration, int(self.audio_engine.sample_rate * self.audio_engine.duration), False)

            # Dynamic Drone Layer with breathing effect
            drone_frequency = 40.0
            breathing_effect = 0.1 * np.sin(0.5 * np.pi * t)
            drone = (0.2 + breathing_effect) * np.sin(2 * np.pi * drone_frequency * t)

            # Melodic Layer with occasional random pitches
            melodic_frequency = drone_frequency * (1 + zoom_level)
            if np.random.rand() < 0.1:
                melodic_frequency += np.random.uniform(-5, 5)
            melodic = 0.1 * np.sin(2 * np.pi * melodic_frequency * t)

            # Echo Effect for Melodic Layer
            delay = int(0.5 * self.audio_engine.sample_rate)
            echo = np.roll(melodic, delay) * 0.6
            melodic += echo

            # Harmonic Overtones with swelling effect
            harmonics = [drone_frequency * (i*3+1) for i in range(3)]
            swell_effect = 0.05 * np.sin(0.2 * np.pi * t)
            harmonic_tones = sum([(0.05 + swell_effect) * np.sin(2 * np.pi * freq * t) for freq in harmonics])

            # Random Ambient Textures
            random_texture = np.interp(t, np.linspace(0, self.audio_engine.duration, 10), np.random.uniform(-0.05, 0.05, 10))

            # Ambient Noise
            noise_intensity = 0.01
            white_noise = noise_intensity * np.random.randn(len(t))

            # Combine all layers
            combined_tone = drone + melodic + harmonic_tones + random_texture + white_noise

            # Apply an envelope for smoothness
            envelope = np.ones_like(combined_tone)
            envelope[:1000] = np.linspace(0, 1, 1000)
            envelope[-1000:] = np.linspace(1, 0, 1000)
            ethereal_tone_with_envelope = combined_tone * envelope

            return ethereal_tone_with_envelope
