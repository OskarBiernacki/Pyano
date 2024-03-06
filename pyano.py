import tkinter as tk
import sys
from SoundMenager import PianoSound

class PyanoWindow():
    piano_notes = ["C","C#","D", "D#", "E", "F","F#","G", "G#", "A", "A#","H"]
    piano_sound=PianoSound()
    def __init__(self):
        print("PyanoWindow creating")
    
    def play_note(self, note):
        print("Playing: {0}".format(note))
        self.piano_sound.play_note(note)

    def create_piano_segment(self, frame ,octava):
        for note in self.piano_notes:
            if '#' in note:
                continue
            button = tk.Button(frame, text=note, width=6, height=8, command=lambda n=note+','+str(octava): self.play_note(n))
            button.pack(side=tk.LEFT, padx=0, anchor="n")

        transform={"C#":25, "D#":59,"F#":127, "G#":163, "A#":198}
        for note in self.piano_notes:
            if '#' not in note:
                continue
            button = tk.Button(frame, text=note, width=3, height=6, command=lambda n=note+','+str(octava): self.play_note(n), bg="#000", fg="#fff")
            button.place(x=transform[note]*1.5, y=0)


    def show_window(self):
        root_window = tk.Tk()
        root_window.title("Pyano")
        root_window.geometry("1200x500")

        top_frame = tk.Frame(root_window, background="#444")
        top_frame.pack(expand=True, fill=tk.BOTH, side='top')

        bottom_frame = tk.Frame(root_window, background="#111")
        bottom_frame.pack(expand=False,fill=tk.BOTH, side='top')

        for oct in range(-2,3,1):
            piano_frame = tk.Frame(bottom_frame, background="#f00")
            piano_frame.pack(expand=False, anchor="s",side="left")
            self.create_piano_segment(piano_frame, oct)

        root_window.mainloop()

if __name__ == "__main__":
    print(sys.version)
    PyanoWindow().show_window()