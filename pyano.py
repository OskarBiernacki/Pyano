import tkinter as tk
from tkinter import * 
import sys
import time
from SoundMenager import PianoSound
import PianoTurotialPlayer as ptp



class PyanoWindow():
    piano_notes = ["C","C#","D", "D#", "E", "F","F#","G", "G#", "A", "A#","H"]
    time_text=None
    piano_sound=PianoSound()
    play_pass_time=0

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

    def milsec_to_timetext(self, milsec) -> str:
        milsec=round(milsec)
        mil=milsec%1000
        sec=(milsec-mil)/1000
        minutes=int(sec//60)
        sec=int(sec%60)
        return "{3}{0}:{4}{1}:{5}{2}".format(int(minutes), int(sec), int(mil), 
                                             '0' if minutes<10 else '',
                                             '0' if sec<10 else '',
                                             '00' if mil<10 else ('0' if mil<100 else '')  )
    
    is_timer_started=False
    def start_timer(self):
        global start_time
        start_time = time.time() * 1000
        self.is_timer_started=True


    def stop_timer(self):
        self.is_timer_started=False


    def show_window(self):
        root_window = tk.Tk()
        root_window.title("Pyano")
        root_window.geometry("1860x700")
        root_window.resizable(True, False)
        setattr(root_window, 'running', True)
        root_window.protocol("WM_DELETE_WINDOW", lambda: setattr(root_window, 'running', False) )

        piano_tutorial = ptp.PianoTutorialPlayer(self.piano_sound)
        
        top_frame = tk.Frame(root_window, background="#444")
        top_frame.pack(expand=True, fill=tk.BOTH, side='top')
        
        #toolbar
        tool_bar = Frame(top_frame, bg="#111")
        tool_bar.pack(side=TOP, fill=X)
        bt=tk.Button(tool_bar, width=3, height=2, text="play",padx=5, command=lambda: f'{piano_tutorial.play_trigger()}{self.start_timer()}' )
        bt.pack(side=LEFT)
        bt=tk.Button(tool_bar, width=3, height=2, text="pause", padx=5, command=lambda: f'{self.stop_timer()}{piano_tutorial.on_reset_screen()}')
        bt.pack(side=LEFT,padx=(2,20))
        box=tk.Text(tool_bar, width=8, height=1, padx=5)
        #box.configure(state=DISABLED) 
        box.insert(1.0,"00:00:00")
        box.pack(side=LEFT)
        self.time_text=box

        #scroll
        scroll = Frame(top_frame, bg="#222")
        scroll.pack(side=RIGHT, fill=Y)
        bt_down=tk.Button(scroll, width=2, height=1, text="V", command=piano_tutorial.on_button_down)
        bt_down.pack(side=BOTTOM)
        bt_top=tk.Button(scroll, width=2, height=1, text="^", command=piano_tutorial.on_button_up)
        bt_top.pack(side=TOP)
        
        #music map
        full_x=0
        move_map = {0:10, 1:30, 2:28, 3:26, 4:30, 5:40, 6:30, 7:28, 8:27, 9:27, 10:28, 11:30}
        for x in range(60):
            full_x+=move_map[x%12]+((0 if x==0 else 30)if x%12==0 else 0)
            for y in range(20):
                t=(x,y)
                bt=tk.Button(top_frame, width=2, height=1, text=x%12+1, bg="#555",
                             command=lambda a=(x,y): piano_tutorial.on_tutor_button_clicked(a) )
                
                bt.place(x=full_x, y=52+26*y)
                piano_tutorial.add_button(bt, t)

        #Piano segment
        bottom_frame = tk.Frame(root_window, background="#111")
        bottom_frame.pack(expand=False,fill=tk.BOTH, side='top')

        for oct in range(-2,3,1):
            piano_frame = tk.Frame(bottom_frame, background="#f00")
            piano_frame.pack(expand=False, anchor="s",side="left")
            self.create_piano_segment(piano_frame, oct)

        #main loop
        while root_window.running:
            root_window.update()
            if self.is_timer_started:
                elasped_time = time.time() * 1000 - start_time
                self.time_text.config(bg="#f00")
                self.time_text.delete(1.0, tk.END)
                play_pass_time=elasped_time
                self.time_text.insert(tk.END, self.milsec_to_timetext(elasped_time))
                piano_tutorial.play_tick(elasped_time)
                #print(self.milsec_to_timetext(elasped_time))
            else:
                self.time_text.config(bg="#fff")


if __name__ == "__main__":
    print(sys.version)
    PyanoWindow().show_window()