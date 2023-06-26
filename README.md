## MIDI to Scribbletune Parser

The objective of this project is to create a scribbletune script which captures a MIDI file as code, so a musician can tweak and render an output MIDI file.

This software is written in python, and currently only creates one pattern. More work is to be done using the Fourier analysis to create mulitple patterns for ease of editing.

## Usage:
```
# example.mid and output.mid must exist in current working directory.
python main.py > tune.js
node tune.js
```

THIS IS FREE SOFTWARE AND COMES WITH ABSOLUTELY NO WARRANTY.
