from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("About this application.")
        layout.addWidget(label)
        self.setLayout(layout)
