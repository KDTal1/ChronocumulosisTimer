import pygame
import numpy as np
import time, threading

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
def note_to_freq(note):
    A4 = 440.0
    note_map = {'C': -9, 'C#': -8, 'D': -7, 'D#': -6, 'E': -5,
                'F': -4, 'F#': -3, 'G': -2, 'G#': -1,
                'A': 0, 'A#': 1, 'B': 2}
    name = note[:-1]
    octave = int(note[-1])
    semitone = note_map[name] + 12 * (octave - 4)
    return A4 * (2.0 ** (semitone / 12.0))

def play_tone(note, duration=0.5, volume=0.2):
    freq = note_to_freq(note)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    waveform = 32767 * volume * np.sin(2 * np.pi * freq * t)

    stereo_waveform = np.column_stack((waveform, waveform))
    sound = pygame.sndarray.make_sound(stereo_waveform.astype(np.int16))
    sound.play(-1)
    time.sleep(duration)
    sound.stop()

def play_custom_tune():
    notes = ["G#4", "A#4", "C#5", "A#4"]
    for n in notes:
        play_tone(n, 0.05)  # each 0.6s

    notes2 = ["F5", "F5", "D#5"]
    for n2 in notes2:
        play_tone(n2, 0.3)

def playTune():
    thread1 = threading.Thread(target=play_custom_tune)
    thread1.start()