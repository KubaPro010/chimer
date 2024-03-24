from pydub import AudioSegment
from pydub.generators import Sine
def generate_beep(duration_ms, frequency): return Sine(frequency).to_audio_segment(duration=duration_ms)
def generate_silence(duration_ms): return AudioSegment.silent(duration=duration_ms)
ending = [
    generate_silence(900),
    generate_beep(500, 1000), 
]
beep_list = []
time = int(input("How many seconds>"))
for i in range(time):
    beep_list.append(generate_silence(900))
    beep_list.append(generate_beep(100, 1000))
beep_list.extend(ending)
format = "mp3"
sum(beep_list).export(f"{time}sec.{format}", format=format)
