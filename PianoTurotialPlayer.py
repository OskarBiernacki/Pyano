import tkinter as tk

class PianoTutorialPlayer:
    buttons={}

    def __init__(self):
        print("PianoTutorialPlayer initieted")

    def add_button(self, button:tk.Button, poz:tuple):
        self.buttons.update({poz:button})

    def on_tutor_button_clicked(self, pozition=(0,0)):
        print(pozition)
        self.buttons[pozition].configure(bg='#f00')
