import PyQt5
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QVBoxLayout, QTextEdit, QComboBox, QDialog, QLineEdit, QMessageBox

# App Info
AppName = "Busqueda Rutas App"
AppDescription = " "
version = "1.0.0"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(AppName + " ver" + version)
        self.setWindowOpacity(0.95)
        self.setGeometry(700,700,500,500)

# Initialize GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setApplicationName(AppName)
    app.setApplicationDisplayName(AppName)
    app.setOrganizationName("Group 6")

    app.setDesktopFileName(AppName)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
