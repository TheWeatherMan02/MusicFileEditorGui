from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout


def horizontal_layout(widget_list):
    """puts individual widgets into a horizontal layout"""
    h_layout = QHBoxLayout()

    for widget in widget_list:
        if isinstance(widget, QWidget):
            h_layout.addWidget(widget)
        elif isinstance(widget, (QVBoxLayout or QHBoxLayout)):
            h_layout.addLayout(widget)

    return h_layout
