from vosk import Model, KaldiRecognizer
import pyaudio as aud
import json

# importing the model, r to save the absolute path
model = Model(r"C:\Users\sara\Desktop\voice_notepad\models\vosk-model-ar-mgb2-0.4")
recognizer = KaldiRecognizer(model, 16000)  #16000 is the frequency

# establishing the mic
mic = aud.PyAudio()
stream = mic.open(format=aud.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

#file to store the text
file = "output.txt"

try:
    with open(file, mode='w', encoding='utf-8') as file:
        while True:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data): # if it  accepts it as a speech
                result = recognizer.Result() # assign the speech to the text
                result_json = json.loads(result)
                text = result_json.get("text", "")
                print(text)
                file.write(text+ " ")

except KeyboardInterrupt:
    print("Stopped, everything is saved in the file")

finally:
    stream.stop_stream()
    stream.close()
    mic.terminate()