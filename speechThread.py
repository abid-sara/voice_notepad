from PyQt5.QtCore import QObject, QThread, pyqtSignal
import os
import sys


if getattr(sys, 'frozen', False):
    # When running from PyInstaller bundle
    dll_path = os.path.join(sys._MEIPASS, 'vosk')
    os.add_dll_directory(dll_path)

from vosk import Model, KaldiRecognizer
import pyaudio
import json


class ArabicSpeechWorker(QObject):
    text_ready = pyqtSignal(str) # signal to send the text to ui
    status_update = pyqtSignal(str) # signal to update the status bar in the ui
    finished = pyqtSignal()   #signal to stop the thread 


    def __init__(self, model_path):
        super().__init__()
        self.model_path = model_path
        self.runing = False
    

    def run(self):
        # if the model is not found quit
        if not os.path.exists(self.model_path):
            self.status_update.emit("Model not found")
            self.finished.emit()
            return
        
        # start listening
        self.runing = True
        self.status_update.emit("Listening...")

        model = Model(self.model_path)
        recognizer = KaldiRecognizer(model, 16000)

        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()

        try:
            while self.runing:
                data = stream.read(4096, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result_json = json.loads(recognizer.Result())
                    text = result_json.get("text", "")
                    if text:
                        self.text_ready.emit(text)
        except Exception as e:
            self.status_update.emit(f"An error occured: {str(e)}") 
        finally:
            stream.stop_stream()
            stream.close()
            mic.terminate()
            self.status_update.emit("Stopped speech recognition")
            self.finished.emit()


    def stop(self):
        self.runing = False               
