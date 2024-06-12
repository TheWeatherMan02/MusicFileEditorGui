from PyQt6.QtWidgets import QComboBox


class DropdownMenu(QComboBox):
    def __init__(self, editor, items, dictionary, save_key, default_image=False):
        super().__init__()

        self.items = items

        if default_image is not False:
            self.default = [editor.default_image['image_label']]
            self.items = self.default + items

        self.addItems(self.items)

        # connect signals to methods
        self.currentTextChanged.connect(lambda: self.changed_value(editor, dictionary, save_key))

    def changed_value(self, editor, dictionary, save_key):
        editor.comm.emit_signal(self.currentText(), save_key, action="le_or_dm_change", dictionary_arg=dictionary)
