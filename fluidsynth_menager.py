import threading
import time
import fluidsynth

class PianoPlayer:
    fs = fluidsynth.Synth()
    fs.start(driver = 'dsound')  # use DirectSound driver
    sfid = fs.sfload(r'Yamaha_C3_Grand_Piano.sf2')  # replace path as needed
    #sfid = fs.sfload(r'FluidR3_GM.sf2')  # replace path as needed
    fs.program_select(0, sfid, 0, 0)

    def play_sound(self, numer_klawisza, duration = 1.0, volume=100):
        self.fs.noteon(0, numer_klawisza, 127)
        self.fs.cc(0, 7, volume)
        time.sleep(duration)
        self.fs.noteoff(0, numer_klawisza)
        time.sleep(1.0)

    def play_note_number(self, number:int, speed):
        threading.Thread(target=self.play_sound, args=(number,speed,127)).start()
    
    def play_note(self, number:str, speed=0.5):
        piano_notes = ["C","C#","D", "D#", "E", "F","F#","G", "G#", "A", "A#","H"]
        note_number = 40
        for i in piano_notes:
            if number.split(',')[0] == i:
                break
            note_number+=1
        note_number+= 12*int(number.split(',')[1]) +12
        print(note_number)
        self.play_note_number(note_number,speed)

if __name__ == '__main__':
    print('piano test')
    p = PianoPlayer()
    for i in range(0,64):
        p.play_note_number(i, 0.2)
        time.sleep(0.2)