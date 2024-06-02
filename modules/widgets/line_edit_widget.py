from PyQt6.QtWidgets import QLineEdit


class LineEditWidget(QLineEdit):
    def __init__(self, external_event):
        super().__init__()
        self.external_event = external_event
        self.textChanged.connect(self.external_event)
