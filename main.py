import mido

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

    # Generate code
    code = 'const scribble = require("scribbletune");\n\n'
    code += 'const clip = scribble.clip({\n'
    code += '    notes: [\n'
    for note, duration in notes:
        if duration > 0:
            note_name = get_note_name(note)
            code += f'        "{note_name}",\n'
    code += '    ],\n'
    code += '    pattern: "x",\n'
    code += '    accentMap: "x---",\n'
    code += '});\n\n'
    code += 'scribble.midi(clip, "output.mid");\n'

    return code

def get_note_name(midi_note):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_note // 12) - 1
    note_index = midi_note % 12
    return note_names[note_index] + str(octave)

# Example usage
midi_file = 'example.mid'
generated_code = parse_midi(midi_file)
print(generated_code)