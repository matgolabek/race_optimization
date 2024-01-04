from gui import MainWindow
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    try:
        app.exec()
    except Exception:
        QMessageBox.critical(window, "Krytyczny błąd", "Aplikacja napotkała straszny błąd",
                             buttons=QMessageBox.StandardButton.Abort)


if __name__ == '__main__':
    main()
