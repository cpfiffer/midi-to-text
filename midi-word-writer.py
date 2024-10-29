# NOTE: you may need to do some adjustments to make sure you
# are using the correct midi port. They are printed out
# so you can see which one you need to use.
import rtmidi
import time
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF

# Dictionary mapping MIDI note numbers to words
# Middle C is note 60
WORD_MAPPING = {
    60: "cat",  # Middle C
    62: "dog",  # D
    64: "bird", # E
    65: "fish", # F
    67: "tree", # G
    69: "sun",  # A
    71: "moon", # B
}

class MidiWordWriter:
    def __init__(self, output_file="output.txt"):
        self.output_file = output_file
        self.midi_in = rtmidi.MidiIn()

        # Check available ports
        available_ports = self.midi_in.get_port_count()
        if available_ports:
            print("Available MIDI ports:")
            for i in range(available_ports):
                print(f"{i}: {self.midi_in.get_port_name(i)}")
        else:
            print("No MIDI ports available!")
            return

        # Open the first available port
        self.midi_in.open_port(1)

        # Set callback function for MIDI input
        self.midi_in.set_callback(self.midi_callback)

    def midi_callback(self, message, time_stamp):
        # print(f"Message: {message}")
        if not message:
            print("Returning")
            return

        # Get message components
        # Message: ([128, 65, 91], 0.274967206)
        # Status: 128, Note: 65, Velocity: 91
        status, note, velocity = message[0]

        # print(f"Status: {status}, Note: {note}")

        # Only process NOTE_ON messages with velocity > 0
        if status == NOTE_ON:
            if note in WORD_MAPPING:
                word = WORD_MAPPING[note]
                self.write_word(word)
                print(f"Note {note} pressed - wrote '{word}' to file")

    def write_word(self, word):
        try:
            with open(self.output_file, 'a') as f:
                f.write(word + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")

    def cleanup(self):
        self.midi_in.close_port()
        self.midi_in = None

if __name__ == "__main__":
    try:
        writer = MidiWordWriter()
        print("\nListening for MIDI input... Press Ctrl+C to exit.")

        # Keep the program running
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nExiting...")
        if writer:
            writer.cleanup()
