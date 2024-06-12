from PyQt6.QtWidgets import QLineEdit


class LineEditWidget(QLineEdit):
    def __init__(self, editor, dictionary, save_key):
        super().__init__()
        self.textChanged.connect(lambda text: self.text_changed(editor, text, save_key, dictionary))

    def text_changed(self, editor, text, save_key, dictionary):
        editor.comm.emit_signal(text, save_key, action="le_or_dm_change", dictionary_arg=dictionary)
