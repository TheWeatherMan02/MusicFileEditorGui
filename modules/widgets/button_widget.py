from PyQt6.QtWidgets import QPushButton


class ButtonWidget(QPushButton):
    def __init__(self, parent, bn_label, action_name, directory_type=None, key=None):
        super().__init__(bn_label)
        self.action_name = action_name
        self.directory_type = directory_type
        self.result = None  # might want key value, but don't need a result
        self.key = key
        self.clicked.connect(lambda: self.button_pushed(parent))

    def button_pushed(self, parent):
        parent.comm.emit_signal(self.result, self.key, action=self.action_name, directory_type=self.directory_type)
