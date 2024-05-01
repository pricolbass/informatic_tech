from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import QTimer
import sys
import os
import fnmatch
from design import Ui_MainWindow


class ImageViewer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_image_index = 0
        self.images = []

        self.load_images_from_folder()

        self.setup_ui()
        self.update_image_display()

    def load_images_from_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            for file in os.listdir(folder):
                if fnmatch.fnmatch(file.lower(), '*.png') or fnmatch.fnmatch(file.lower(), '*.jpg') or fnmatch.fnmatch(
                        file.lower(), '*.jpeg') or fnmatch.fnmatch(file.lower(), '*.bmp') or fnmatch.fnmatch(
                    file.lower(), '*.gif'):
                    self.images.append(os.path.join(folder, file))
            self.images.sort()

    def setup_ui(self):
        self.prev_button.clicked.connect(self.prev_image)
        self.next_button.clicked.connect(self.next_image)
        self.first_button.clicked.connect(self.first_image)
        self.last_button.clicked.connect(self.last_image)
        self.slide_show_button.clicked.connect(self.start_slide_show)
        self.rotate_button.clicked.connect(self.rotate_image)
        self.delete_button.clicked.connect(self.delete_image)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image)

    def update_image_display(self):
        if self.images:
            pixmap = QPixmap(self.images[self.current_image_index])
            self.image_label.setPixmap(pixmap)  # Установите изображение на QLabel
            self.setWindowTitle(f"Image Viewer - {os.path.basename(self.images[self.current_image_index])}")
        self.update_buttons()

    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.update_image_display()

    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.update_image_display()
        else:
            self.current_image_index = 0
            self.update_image_display()

    def first_image(self):
        self.current_image_index = 0
        self.update_image_display()

    def last_image(self):
        self.current_image_index = len(self.images) - 1
        self.update_image_display()

    def start_slide_show(self):
        if self.timer.isActive():
            self.timer.stop()
            self.slide_show_button.setText("Slide Show")
        else:
            self.timer.timeout.connect(self.next_image)
            self.timer.start(2000)  # Change the image every 2 seconds
            self.slide_show_button.setText("Stop")

    def rotate_image(self):
        if not self.images:
            return

        pixmap = QPixmap(self.images[self.current_image_index])
        transform = QTransform().rotate(90)
        rotated_pixmap = pixmap.transformed(transform)
        rotated_pixmap.save(self.images[self.current_image_index])
        self.update_image_display()

    def delete_image(self):
        if not self.images or self.current_image_index >= len(self.images):
            return

        confirm_delete = QMessageBox.question(self, "Delete Image", "Are you sure you want to delete this image?",
                                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm_delete == QMessageBox.StandardButton.Yes:
            image_to_delete = self.images.pop(self.current_image_index)
            os.remove(image_to_delete)
            if self.current_image_index == len(self.images) and self.current_image_index != 0:
                self.current_image_index -= 1
            self.update_image_display()

    def update_buttons(self):
        self.prev_button.setEnabled(self.current_image_index > 0)
        self.next_button.setEnabled(self.current_image_index < len(self.images) - 1)
        self.first_button.setEnabled(self.current_image_index > 0)
        self.last_button.setEnabled(self.current_image_index < len(self.images) - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())
