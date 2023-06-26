import mido
import numpy as np
from scipy.fft import rfft, rfftfreq

def parse_midi(file_path):
    # Load MIDI file
    mid = mido.MidiFile(file_path)

    # Extract note events
    notes = []
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':
                if msg.velocity > 0:
                    notes.append((msg.note, msg.time))
                else:
                    # Note off event
                    notes.append((msg.note, 0))

    # Separate note durations
    durations = [duration for _, duration in notes]

    # Perform Fourier Transform
    signal = np.array(durations)
    fft = rfft(signal)
    frequencies = rfftfreq(len(signal))

    # Find dominant frequencies
    dominant_indices = np.argsort(np.abs(fft))[-5:]  # Adjust the number of dominant frequencies to consider
    dominant_frequencies = frequencies[dominant_indices]

    # Assign note durations to patterns
    pattern_map = {}
    for duration in durations:
        closest_frequency = min(dominant_frequencies, key=lambda f: abs(f - duration))
        pattern_index = np.where(dominant_frequencies == closest_frequency)[0][0]
        pattern_map.setdefault(pattern_index, []).append(duration)

    # Generate code
    code = 'const scribble = require("scribbletune");\n\n'
    code += 'const clip = scribble.clip({\n'
    code += '    pattern: [\n'
    for pattern_index, pattern_durations in pattern_map.items():
        pattern_durations_str = ', '.join([str(duration) for duration in pattern_durations])
        code += f'        "{pattern_durations_str}",\n'
    code += '    ],\n'
    code += '    notes: ["C4"],\n'  # Adjust the notes as per your requirement
    code += '    patternLength: 8,\n'  # Adjust the pattern length as per your requirement
    code += '    accentMap: "x---",\n'
    code += '});\n\n'
    code += 'scribble.midi(clip, "output.mid");\n'

    return code

# Example usage
midi_file = 'example.mid'
generated_code = parse_midi(midi_file)
print(generated_code)
