from voiceNotepadUI import VoiceNotepad
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/voice_record.ico"))
    window = VoiceNotepad()
    window.show()
    sys.exit(app.exec_())
