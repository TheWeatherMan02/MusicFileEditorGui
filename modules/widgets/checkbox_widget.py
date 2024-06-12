from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt


class CheckboxWidget(QCheckBox):
    def __init__(self, cb_label, editor):
        super().__init__(cb_label)
        self.setCheckState(Qt.CheckState.Unchecked)
        self.stateChanged.connect(self.check_state_changed)

    def check_state_changed(self):
        print(f"check state changed to: {self.checkState()}")
