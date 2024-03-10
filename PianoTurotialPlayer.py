import tkinter as tk
from queue import PriorityQueue
from SoundMenager import PianoSound as ps

class PianoTutorialPlayer:

    nouts_to_play = PriorityQueue()

    segment_time_value=250
    current_screen_time=0

    buttons={}
    buttons_state={}
    buttons_active=[]

    piano_sound_menager=None

    def __init__(self, piano_sound_menager):
        self.piano_sound_menager=piano_sound_menager
        print("PianoTutorialPlayer initieted")

    def set_button(self, button:tk.Button, state:bool):
        if state:
            button.configure(bg='#f00')
            self.buttons_active.insert(0,button)
        else:
            button.configure(bg='#555')
            self.buttons_active.remove(button)
        self.buttons_state[button]=state

    ###
    def add_button(self, button:tk.Button, poz:tuple):
        self.buttons.update({poz:button})
        self.buttons_state.update({button:False})
    def column_number_to_note(self, column_number)->str:
        piano_notes = ["C","C#","D", "D#", "E", "F","F#","G", "G#", "A", "A#","H"]
        out=piano_notes[column_number%12]+","+str(column_number//12-2)
        return out
    def row_to_time(self, row_number):
        return (19-row_number)*self.segment_time_value + self.current_screen_time
    def on_tutor_button_clicked(self, pozition=(0,0)):
        time_stamp_sound=(self.row_to_time(pozition[1]), self.column_number_to_note(pozition[0]))
        if self.buttons_state[self.buttons[pozition]]==False:
            print('Add:',time_stamp_sound)
            self.set_button(self.buttons[pozition], True)
            self.nouts_to_play.put(time_stamp_sound)
        else:
            print('Del:',time_stamp_sound)
            self.set_button(self.buttons[pozition], False)
            self.nouts_to_play.queue.remove(time_stamp_sound)

    ####
    def repaint_buttons(self):
        #print('repainting...')
        #reset colors
        for button in self.buttons_active.copy():
            self.set_button(button, False)
        
        painting_range = (self.row_to_time(19), self.row_to_time(0))
        #print('printing range:', painting_range)

        for item in self.nouts_to_play.queue:
            #print(item)
            poz_y=(item[0]-painting_range[0])//self.segment_time_value
            poz_y=19-poz_y
            poz_x=0
            for i in range(0,60):
                if self.column_number_to_note(i) == item[1]:
                    poz_x=i
            if poz_x in range(0,60) and poz_y in range(0,20):
                #print('[{0}, {1}]'.format(poz_x,poz_y))
                bt=self.buttons[(poz_x,poz_y)]
                self.set_button(bt, True)

    def on_button_up(self, steps:int=2):
        self.current_screen_time+=self.segment_time_value*steps
        self.repaint_buttons()
    def on_button_down(self, steps:int=2):
        if self.current_screen_time>0:
            self.current_screen_time-=self.segment_time_value*steps
            self.repaint_buttons()
    def on_reset_screen(self):
        self.current_screen_time=0
        self.repaint_buttons()
    def on_reset_button(self):
        self.nouts_to_play = PriorityQueue()
        self.on_reset_screen()

    to_play=None
    item_to_play=None
    def play_trigger(self):
        print('Start palying!')
        self.on_reset_screen()
        self.to_play=self.nouts_to_play.queue.copy()
        self.to_play.sort()
        self.to_play.reverse()
        print(self.to_play)
        if len(self.to_play)>0:
            self.item_to_play=self.to_play.pop()
    def play_tick(self, time:int=0):
        time = round(time)
        #step
        if self.current_screen_time < (time//self.segment_time_value)*self.segment_time_value:
            while self.item_to_play != None and self.item_to_play[0] <= self.current_screen_time:
                print('play:',self.item_to_play)
                self.piano_sound_menager.play_note(self.item_to_play[1])
                #self.piano_sound_menager.play_note(self.item_to_play[1],0.5)
                if len(self.to_play)>0:
                    self.item_to_play=self.to_play.pop()
                else:
                    self.item_to_play=None

            self.current_screen_time+=self.segment_time_value
            self.repaint_buttons()
    
    ### Saving 
    def save_list_to_file(self, file_path):
        try:
            data_list=self.nouts_to_play.queue
            with open(file_path, 'w') as file:
                for item in data_list:
                    file.write(f"{item[0]}%{item[1]}\n")
            print("Saved to ->",file_path)
        except Exception as e:
            print(f"Saving error: {e}")

    def read_list_from_file(self, file_path):
        try:
            data_list = []
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split('%')
                    if len(parts) == 2:
                        data_list.append((int(parts[0]), parts[1]))
            self.nouts_to_play=PriorityQueue()
            print(data_list)
            for item in data_list:
                self.nouts_to_play.put(item)
            self.on_reset_screen()
            print('save readed OK')
        except Exception as e:
            print(f"file read errorr: {e}")