import tkinter as tk
from tkinter import * 
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
        root_window.geometry("1860x700")
        root_window.resizable(True, False)



        top_frame = tk.Frame(root_window, background="#444")
        top_frame.pack(expand=True, fill=tk.BOTH, side='top')
        
        tool_bar = Frame(top_frame, bg="#111")
        tool_bar.pack(side=TOP, fill=X)
        bt_play=tk.Button(tool_bar, width=3, height=2, text="play")
        bt_play.pack(side=TOP)


        scroll = Frame(top_frame, bg="#222")
        scroll.pack(side=RIGHT, fill=Y)
        bt_down=tk.Button(scroll, width=2, height=1, text="V")
        bt_down.pack(side=BOTTOM)
        bt_top=tk.Button(scroll, width=2, height=1, text="^")
        bt_top.pack(side=TOP)
        
        full_x=0
        move_map = {0:10, 1:30, 2:28, 3:26, 4:30, 5:40, 6:30, 7:28, 8:27, 9:27, 10:28, 11:30}
        for x in range(60):
            full_x+=move_map[x%12]+((0 if x==0 else 30)if x%12==0 else 0)
            for y in range(20):
                bt=tk.Button(top_frame, width=2, height=1, text=x%12+1)
                bt.configure(bg="#555")
                bt.place(x=full_x, y=52+26*y)

        #Piano segment
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