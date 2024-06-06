from PyQt6.QtWidgets import QLineEdit


class LineEditWidget(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.textChanged.connect(lambda text: self.text_changed(parent, text))

    def text_changed(self, parent, text):
        parent.comm.emit_signal(text, action="le_or_dm_change")
