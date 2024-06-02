from PyQt6.QtWidgets import QComboBox


class DropdownMenu(QComboBox):
    def __init__(self, items, external_event):
        super().__init__()

        self.items = items
        self.addItems(self.items)

        self.external_event = external_event

        # connect signals to methods
        self.currentTextChanged.connect(self.external_event)

    # def func(self):
    #     self.text = self.currentText()
    #     print(self.text)
