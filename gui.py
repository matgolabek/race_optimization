from data import *
import sys
from population import *
from typing import List
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, \
    QFileDialog, QComboBox, QLineEdit, QGroupBox, QTabWidget, QLabel, QPushButton, QDialog, QDialogButtonBox, \
    QDoubleSpinBox, QSpinBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSlot


# OKNO GŁÓWNE

class MainWindow(QMainWindow):

    def __init__(self):
        """
        Okno główne, wyświetlające aplikacje
        """
        super(MainWindow, self).__init__()

        # DANE

        self.circuit = None
        self.circuit_name = ''
        self.circuit_track_distance = 0
        self.circuit_no_laps = 0
        self.circuit_t_pit = 0.
        self.circuit_tires = []

        # ZMIENNE ALGORYTMU

        self.iterations = 0

        # USTAWIENIA OKNA

        self.resize(800, 600)  # rozmiar
        self.setWindowTitle('Race optimization')  # nazwa okna

        tabs = QTabWidget()  # zakładki Konfiguracja, Rozwiązanie, Wykres
        tabs.setTabPosition(QTabWidget.TabPosition.North)  # pozycja zakłedek
        tabs.setMovable(False)  # przemieszczanie zakładek

        tabs.addTab(Config(self), 'Konfiguracja')  # dodanie zakładki Konfiguracja
        tabs.addTab(Solution(self), 'Rozwiązanie')  # dodanie zakładki Arkusz
        tabs.addTab(Chart(self), 'Wykres')  # dodanie zakładek Wykres

        self.setCentralWidget(tabs)  # umieszczenie zakładek w oknie


# ZAKŁADKI

class Config(QWidget):

    def __init__(self, parent: MainWindow):
        """
        Zakładka z konfiguracją danych do algorytmu
        :param parent: (QMainWindow) okno rodzic
        """
        super(Config, self).__init__()

        self.parent = parent

        layout_main = QHBoxLayout()  # układ główny
        box_circuit = QGroupBox('Dane wyścigu')  # układ z danymi wyścigu
        layout_circuit = QFormLayout()
        box_config = QGroupBox('Parametry algorytmu')  # układ z konfiguracją algorytmu
        layout_config = QVBoxLayout()

        layout_main.setContentsMargins(20, 20, 20, 20)  # wielkość ramki
        layout_main.setSpacing(20)  # odległości między widżetami

        layout_circuit.addRow('Nazwa:', QLineEdit(self.parent.circuit_name, self))
        spin_no_laps = QSpinBox(self)
        spin_no_laps.setValue(self.parent.circuit_no_laps)
        layout_circuit.addRow('Liczba okrążeń:', spin_no_laps)
        spin_track_dist = QSpinBox(self)
        spin_track_dist.setValue(self.parent.circuit_track_distance)
        layout_circuit.addRow('Długość toru [m]:', spin_track_dist)
        spin_t_pit = QDoubleSpinBox(self)
        spin_t_pit.setValue(self.parent.circuit_t_pit)
        spin_t_pit.setDecimals(3)
        layout_circuit.addRow('Czas pit stopu [s]:', spin_t_pit)

        # layout_config - przyciski
        button_read = QPushButton("Wczytaj dane z pliku")   # wczytywanie z pliku
        button_read.setFixedSize(200, 50)
        #button_read.clicked.connect()

        button_write = QPushButton("Zapisz wprowadzone dane")   # zapisywanie do pliku
        button_write.setFixedSize(200, 50)

        layout_config.addWidget(button_read)    # dodanie prrzycisków do layoutu
        layout_config.addWidget(button_write)

        # USTAWIENIA UKŁADU
        box_circuit.setLayout(layout_circuit)
        box_config.setLayout(layout_config)
        layout_main.addWidget(box_circuit)
        layout_main.addWidget(box_config)
        self.setLayout(layout_main)

    def choose_file(self) -> None:
        pass


class Solution(QWidget):

    def __init__(self, parent: MainWindow):
        """
        Zakładka z rozwiązaniem
        :param parent: (QMainWindow) : okno rodzic
        """
        super(Solution, self).__init__()

        self.parent = parent  # wskaźnik na rodzica

        layout_main = QVBoxLayout()  # układ główny

        # USTAWIENIA UKŁADU
        self.setLayout(layout_main)


class Chart(QWidget):

    def __init__(self, parent: MainWindow):
        """
        Zakładka z wykresem wartości funkcji celu od iteracji
        :param parent: (QMainWindow) : okno rodzic
        """
        super(Chart, self).__init__()

        self.parent = parent  # wskaźnik na rodzica

        layout_main = QVBoxLayout()  # układ główny

        # USTAWIENIA UKŁADU
        self.setLayout(layout_main)



def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    try:
        app.exec()
    except Exception:
        QMessageBox.critical(window, "Krytyczny błąd", "Aplikacja napotkała straszny błąd",
                             buttons=QMessageBox.StandardButton.Abort)


if __name__ == "__main__":
    main()
