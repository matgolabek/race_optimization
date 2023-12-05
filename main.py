from data import *
import sys
from typing import List
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, \
    QFileDialog, QComboBox, QTableWidget, QTableWidgetItem, QTabWidget, QLabel, QPushButton, QDialog, QDialogButtonBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSlot


class MainWindow(QMainWindow):

    def __init__(self):
        """
        Okno główne, wyświetlające aplikacje
        """
        super(MainWindow, self).__init__()

        self.circuit = load_data("Circuits/Jeddah.pkl")

        self.resize(800, 600)  # rozmiar
        self.setWindowTitle('Race optimization')  # nazwa okna

        tabs = QTabWidget()  # zakładki Konfiguracja, Arkusz, Wykres
        tabs.setTabPosition(QTabWidget.TabPosition.North)  # pozycja zakłedek
        tabs.setMovable(False)  # przemieszczanie zakładek

        #tabs.addTab(Config(self), 'Konfiguracja')  # dodanie zakładki Konfiguracja
        #tabs.addTab(Sheet(self), 'Arkusz kalkulacyjny')  # dodanie zakładki Arkusz
        #tabs.addTab(Chart(self), 'Wykres')  # dodanie zakładek Wykres

        self.setCentralWidget(tabs)  # umieszczenie zakładek w oknie


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
