from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QCheckBox, QSizePolicy
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt


class CustomizationPopup(QDialog):
    def __init__(self, current_font: QFont, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Customize Text")
        self.setFixedSize(500, 360)

        self.setStyleSheet("""
        QDialog {
            background-color: #fcfcfc;
            
        }

        QLabel {
            color: #222;
            background-color: transparent;
            font-size: 26px;
        }

        QComboBox {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            min-width: 150px;
            font-size: 26px;
            background-color: transparent;
        }

        QCheckBox {
            font-size: 26px;
            spacing: 10px;
            background-color: transparent;
        }

        QCheckBox::indicator {
            width: 22px;
            height: 22px;
        }

        QPushButton {
            padding: 10px 20px;
            background-color: #f5f5c7;
            border-radius: 8px;
            border: 1px solid #bbb;
            font-size: 26px;
        }

        QPushButton:hover {
            background-color: #ececab;
        }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 20)

        # Font family
        font_layout = QHBoxLayout()
        font_label = QLabel("Font:")
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Tahoma", "Times New Roman", "Courier New"])
        self.font_combo.setCurrentText(current_font.family())
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_combo)
        layout.addLayout(font_layout)

        # Font size
        size_layout = QHBoxLayout()
        size_label = QLabel("Size:")
        self.size_combo = QComboBox()
        self.size_combo.addItems(["10", "12", "14", "16", "18", "20", "24", "28", "32"])
        self.size_combo.setCurrentText(str(current_font.pointSize()))
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_combo)
        layout.addLayout(size_layout)

        # Font style checkboxes
        style_layout = QHBoxLayout()
        self.bold_checkbox = QCheckBox("Bold")
        self.bold_checkbox.setChecked(current_font.bold())

        self.italic_checkbox = QCheckBox("Italic")
        self.italic_checkbox.setChecked(current_font.italic())

        self.underline_checkbox = QCheckBox("Underline")
        self.underline_checkbox.setChecked(current_font.underline())

        style_layout.addWidget(self.bold_checkbox)
        style_layout.addWidget(self.italic_checkbox)
        style_layout.addWidget(self.underline_checkbox)
        layout.addLayout(style_layout)

        # Apply button (centered with auto width)
        self.apply_button = QPushButton("Apply")
        self.apply_button.setCursor(Qt.PointingHandCursor)
        self.apply_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.apply_button, alignment=Qt.AlignCenter)

        self.apply_button.clicked.connect(self.accept)
        self.setLayout(layout)

    def get_values(self):
        return {
            "font_family": self.font_combo.currentText(),
            "font_size": int(self.size_combo.currentText()),
            "bold": self.bold_checkbox.isChecked(),
            "italic": self.italic_checkbox.isChecked(),
            "underline": self.underline_checkbox.isChecked()
        }
