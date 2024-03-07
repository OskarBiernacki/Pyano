from pydub.generators import Sine
from pydub.playback import play
import wave
import pyaudio
import math
import threading

class PianoSound:
    piano_notes_value = {"C":261.63,"C#":277.18,"D":293.66, "D#":311.13, 
                         "E":329.63, "F":349.23,"F#":369.99,"G":392.00, 
                         "G#":415.30, "A":440.00, "A#":466.16,"H":493.88}
        

    def __init__(self):
        print("Creating sounds...")
        for n in range(1, 89):
            file_to_create='sounds/sound-'+str(n)+"-"+str(round(self.n_to_frequency(n)))+".wav"
            self.create_wav(self.n_to_frequency(n), file_to_create)
    
    #n to numer klawisza
    def n_to_frequency(self, n) -> float:
        return 2**((n-49)/12)*440
    

    def frequency_to_n(self, frequency)-> int:
        return round(12 * math.log2(frequency / 440) + 49)
    

    def create_wav(self, frequency, file_name):
        print('+'+file_name)
        tone=Sine(frequency).to_audio_segment(200,volume=-15)
        tone.export(file_name, format="wav")


    def play_wav(self, file_name):
        chunk = 1024  
        f = wave.open(file_name,"rb")  
        p = pyaudio.PyAudio()  
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)  
        data = f.readframes(chunk)  
        while data:  
            stream.write(data)  
            data = f.readframes(chunk)  
        stream.stop_stream()  
        stream.close()  
        p.terminate() 


    def play_note(self, midi_note):
        note=self.piano_notes_value[midi_note.split(',')[0]]
        quart= midi_note.split(',')[1] 
        noute_number = self.frequency_to_n(note)+int(quart)*12
        note=self.n_to_frequency(noute_number)
    
        file_to_play='sounds/sound-'+str(noute_number)+'-'+str(round(note))+".wav"
        threading.Thread(target=self.play_wav, args=(file_to_play,)).start()


if __name__ == '__main__':
    PianoSound().play_note("C,0")
