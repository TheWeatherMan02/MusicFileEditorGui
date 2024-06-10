from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap


class ImageWidget(QGroupBox):
    def __init__(self, image, box_title):
        super().__init__(box_title)

        self.image_label = QLabel(self)
        pixmap = QPixmap(image)

        self.image_label.setPixmap(pixmap)
        self.image_label.resize(pixmap.width(), pixmap.height())

        v_layout_image = QVBoxLayout()
        v_layout_image.addWidget(self.image_label)
        self.setLayout(v_layout_image)
