import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QSizePolicy, QFileDialog, QMessageBox, QDialog, QLineEdit
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QTextCharFormat
from PyQt5.QtCore import Qt, QThread, QStandardPaths
from speechThread import ArabicSpeechWorker
from docx import Document
from customizePopup import CustomizationPopup

class VoiceNotepad(QWidget):
    "This is the UI class along with the functions of the buttons functionalities"
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline Arabic Voice Notepad")
        self.setWindowIcon(QIcon("assets/voice_record.ico"))
        self.showMaximized()
        self.setStyleSheet("background-color: #f5f5f5;")
        self.thread = None
        self.worker = None

        self.init_ui()

    def load_icon(self, path, size=(30, 30)):
        pixmap = QPixmap(path).scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QIcon(pixmap)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        #toolbar
        toolbar = QHBoxLayout()

        btn_style = """
            QPushButton {
                height: 40px;
                background-color: #f5f5c7;
                font-size: 23px;
                color: #161616;
                padding: 8px;
                border: none;
                border-radius: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #ececab;
            }
        """

        self.start_btn = QPushButton(" Start")
        self.start_btn.setIcon(self.load_icon("assets/start.png"))
        self.start_btn.setStyleSheet(btn_style)
        self.start_btn.clicked.connect(self.start_recording)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        
        self.stop_btn = QPushButton(" Stop")
        self.stop_btn.setIcon(self.load_icon("assets/stop.png"))
        self.stop_btn.setStyleSheet(btn_style)
        self.stop_btn.clicked.connect(self.stop_recording)
        self.stop_btn.setCursor(Qt.PointingHandCursor)

        self.save_btn = QPushButton(" Save")
        self.save_btn.setIcon(self.load_icon("assets/save.png"))
        self.save_btn.setStyleSheet(btn_style)
        self.save_btn.clicked.connect(self.save_file)
        self.save_btn.setCursor(Qt.PointingHandCursor)

        self.new_btn = QPushButton(" New")
        self.new_btn.setIcon(self.load_icon("assets/new.png"))
        self.new_btn.setStyleSheet(btn_style)
        self.new_btn.clicked.connect(self.new_file)
        self.new_btn.setCursor(Qt.PointingHandCursor)

        self.customize_btn = QPushButton(" Customize")
        self.customize_btn.setIcon(self.load_icon("assets/customize.png"))
        self.customize_btn.setStyleSheet(btn_style)
        self.customize_btn.clicked.connect(self.customize_text)
        self.customize_btn.setCursor(Qt.PointingHandCursor)

        for btn in [self.start_btn, self.stop_btn, self.save_btn, self.new_btn, self.customize_btn]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            toolbar.addWidget(btn)

        layout.addLayout(toolbar)
        self.set_button_states(False)

        #file name section
        self.filename_input = QLineEdit("")
        self.filename_input.setPlaceholderText("Enter filename")
        self.filename_input.setMinimumWidth(600)
        self.filename_input.setStyleSheet("""
            QLineEdit {
                font-size: 23px;
                padding: 10px;
                border: 1px solid #9ea2a3;
                border-radius: 6px;
                background-color: #fffbe6;
            }
            """)
        self.filename_input.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.filename_input, alignment = Qt.AlignCenter)

        #text area
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Arial", 14))
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: #222;
            }
        """)
       
        layout.addWidget(self.text_edit)

        #status bar
        self.status = QLabel("Status: Idle")
        self.status.setStyleSheet("background-color: #fafafa; padding: 5px; font-size: 20px; color: #161616;")
        layout.addWidget(self.status)

        self.setLayout(layout)


    def set_button_states(self, recording_state:bool):
        "This method will make all buttons freeze during live record except the stop button"

        self.start_btn.setEnabled(not recording_state)
        self.stop_btn.setEnabled(recording_state)
        self.save_btn.setEnabled(not recording_state)
        self.new_btn.setEnabled(not recording_state)
        self.customize_btn.setEnabled(not recording_state)


    def insert_transcribed_text(self, text):
        "Insert text at the current cursor position"
        self.text_edit.insertPlainText(" " + text)
        

    #Button functionalities
    def start_recording(self):
        
        self.thread = QThread()
        model_path = os.path.join(os.path.dirname(__file__), "models", "vosk-model-ar-mgb2-0.4")
        self.worker = ArabicSpeechWorker(model_path)
        self.worker.moveToThread(self.thread)

        # connect thread events
        self.thread.started.connect(self.worker.run)
        self.worker.text_ready.connect(self.insert_transcribed_text)
        self.worker.status_update.connect(self.status.setText)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.set_button_states(True)  # set the button state to record mode

        
    def stop_recording(self):
        if self.worker:
            self.worker.stop()
            self.status.setText("Status: Idle")
            self.set_button_states(False)

            

    def save_file(self):
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        
        filename = self.filename_input.text().strip()

        if not filename:
            filename = "document.docx"
        
        selected_path = os.path.join(desktop_path, filename)
        
        #Showing the dialog for saving the file into .docx
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            selected_path,
            "Word Documents (*.docx)"
        )

        if path:
            if not path.endswith(".docx"):
                path += ".docx"
            
            try:
                doc = Document()
                doc.add_paragraph(self.text_edit.toPlainText())
                doc.save(path)

                QMessageBox.information(self, "Saved", f"File saved to: {path}")
            except Exception as e:
                QMessageBox.information(self,  "Error", f"Failed to save the file :{e}") 


    def new_file(self):
        "This will verify if there is a txt, if yes it will alarm"
        current_text = self.text_edit.toPlainText().strip()

        if current_text:
            reply = QMessageBox.question(
                self,
                "Confirm New File",
                "⚠️ Unsaved text will be lost. Do you want to continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No   # default selected button
            )

            if reply == QMessageBox.No:
                return
        
        self.text_edit.clear()
        self.filename_input.clear()
        self.status.setText("New file created")

    def customize_text(self):
        current_font = self.text_edit.currentFont()
        dialog = CustomizationPopup(current_font, self)

        if dialog.exec_() != QDialog.Accepted:
            return
           
        values = dialog.get_values()

        #creating character with the new customization for new input
        format = QTextCharFormat()
        format.setFontFamily(values["font_family"])
        format.setFontPointSize(values["font_size"])
        format.setFontWeight(QFont.Bold if values["bold"] else QFont.Normal)
        format.setFontItalic(values["italic"])
        format.setFontUnderline(values["underline"])


        #applying customization to selected text
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            cursor.mergeCharFormat(format)
        else:
            self.text_edit.setCurrentCharFormat(format)







