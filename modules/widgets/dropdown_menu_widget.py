from PyQt6.QtWidgets import QComboBox


class DropdownMenu(QComboBox):
    def __init__(self, items, parent):
        super().__init__()

        self.items = items
        self.addItems(self.items)

        # self.external_event = external_event

        # connect signals to methods
        self.currentTextChanged.connect(lambda: self.changed_value(parent))

    def changed_value(self, parent):
        parent.comm.emit_signal(self.currentText(), action="le_or_dm_change")
