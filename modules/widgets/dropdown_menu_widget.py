from PyQt6.QtWidgets import QComboBox


class DropdownMenu(QComboBox):
    def __init__(self, parent, items, dictionary, save_key, default_image=False):
        super().__init__()

        self.items = items

        if default_image is not False:
            self.default = ["-- Default --"]
            self.items = self.default + items

        self.addItems(self.items)

        # connect signals to methods
        self.currentTextChanged.connect(lambda: self.changed_value(parent, dictionary, save_key))

    def changed_value(self, parent, dictionary, save_key):
        parent.comm.emit_signal(self.currentText(), save_key, action="le_or_dm_change", dictionary_arg=dictionary)
