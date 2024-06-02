from PyQt6.QtWidgets import QPushButton


class ButtonWidget(QPushButton):
    def __init__(self, bn_label, external_event, parent=None):
        super().__init__(bn_label, parent)
        self.external_event = external_event
        self.clicked.connect(self.external_event)
