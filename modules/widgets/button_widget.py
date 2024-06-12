from PyQt6.QtWidgets import QPushButton


class ButtonWidget(QPushButton):
    def __init__(self, editor, bn_label, action_name, dictionary=None, key=None):
        super().__init__(bn_label)
        self.action_name = action_name
        self.dictionary = dictionary
        self.result = None  # might want key value, but don't need a result
        self.key = key
        self.clicked.connect(lambda: self.button_pushed(editor))

    def button_pushed(self, editor):
        editor.comm.emit_signal(self.result, self.key, action=self.action_name, dictionary_arg=self.dictionary)
