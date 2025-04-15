import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from UILogic.mainwindow_ui import Ui_MainWindow

#test

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect_signals()
        self.image_path = None

    def connect_signals(self):
        self.btnUpload.clicked.connect(self.upload_image)
        self.btnRotate.clicked.connect(self.rotate_image)
        self.btnCrop.clicked.connect(self.crop_image)
        self.btnSave.clicked.connect(self.save_image)
        self.btnDelete.clicked.connect(self.delete_image)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.labelPreview.setPixmap(pixmap.scaled(self.labelPreview.size()))
            QMessageBox.information(self, "Upload", f"Uploaded: {file_path}")

    def rotate_image(self):
        QMessageBox.information(self, "Rotate", "Rotate image (demo only)")

    def crop_image(self):
        QMessageBox.information(self, "Crop", "Crop image (demo only)")

    def save_image(self):
        QMessageBox.information(self, "Save", "Save image (demo only)")

    def delete_image(self):
        self.labelPreview.clear()
        self.image_path = None
        QMessageBox.information(self, "Delete", "Image deleted")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
