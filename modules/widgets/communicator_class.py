from PyQt6.QtCore import pyqtSignal, QObject


class Communicator(QObject):
    my_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def emit_signal(self, *args, **kwargs):
        self.my_signal.emit((args, kwargs))
