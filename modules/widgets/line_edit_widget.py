from PyQt6.QtWidgets import QLineEdit


class LineEditWidget(QLineEdit):
    def __init__(self, parent, dictionary, save_key):
        super().__init__()
        self.textChanged.connect(lambda text: self.text_changed(parent, text, save_key, dictionary))

    def text_changed(self, parent, text, save_key, dictionary):
        parent.comm.emit_signal(text, save_key, action="le_or_dm_change", dictionary_arg=dictionary)
