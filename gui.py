from data import *
import sys
from population import *
from typing import List, Any
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, \
    QFileDialog, QComboBox, QLineEdit, QGroupBox, QTabWidget, QLabel, QPushButton, QDialog, QDialogButtonBox, \
    QDoubleSpinBox, QSpinBox, QListWidget, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSlot, QRect


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
        self.box_circuit = QGroupBox('Dane wyścigu')  # układ z danymi wyścigu
        self.layout_circuit = QFormLayout()
        box_config = QGroupBox('Parametry algorytmu')  # układ z konfiguracją algorytmu
        layout_config = QVBoxLayout()

        layout_main.setContentsMargins(20, 20, 20, 20)  # wielkość ramki
        layout_main.setSpacing(20)  # odległości między widżetami

        self.layout_circuit.addRow('Nazwa:', QLineEdit(self.parent.circuit_name, self))
        spin_no_laps = QSpinBox(self)
        spin_no_laps.setValue(self.parent.circuit_no_laps)
        self.layout_circuit.addRow('Liczba okrążeń:', spin_no_laps)
        spin_track_dist = QSpinBox(self)
        spin_track_dist.setRange(0, 99999)
        spin_track_dist.setValue(self.parent.circuit_track_distance)
        spin_track_dist.setSuffix(" m")
        self.layout_circuit.addRow('Długość toru:', spin_track_dist)
        spin_t_pit = QDoubleSpinBox(self)
        spin_t_pit.setValue(self.parent.circuit_t_pit)
        spin_t_pit.setDecimals(3)
        spin_t_pit.setSuffix(" s")
        self.layout_circuit.addRow('Czas pit stopu:', spin_t_pit)

        self.list_tires = QListWidget(self)
        self.list_tires.setFixedHeight(400)
        add_button = QPushButton("Dodaj")
        add_button.clicked.connect(self.add)
        remove_button = QPushButton("Usuń")
        remove_button.clicked.connect(self.remove)
        edit_button = QPushButton("Edytuj")
        edit_button.clicked.connect(self.edit)
        clear_button = QPushButton("Wyczyść")
        clear_button.clicked.connect(self.clear)
        tires_layout = QGridLayout()
        tires_layout.addWidget(self.list_tires, 0, 0, 10, 1)
        tires_layout.addWidget(add_button, 0, 1)
        tires_layout.addWidget(edit_button, 1, 1)
        tires_layout.addWidget(remove_button, 2, 1)
        tires_layout.addWidget(clear_button, 3, 1)
        self.layout_circuit.addRow('Opony:', tires_layout)

        # layout_config - przyciski
        button_read = QPushButton("Wczytaj dane z pliku")   # wczytywanie z pliku
        button_read.setFixedSize(200, 50)
        button_read.clicked.connect(self.choose_file)

        button_write = QPushButton("Zapisz wprowadzone dane")   # zapisywanie do pliku
        button_write.setFixedSize(200, 50)

        layout_config.addWidget(button_read)    # dodanie prrzycisków do layoutu
        layout_config.addWidget(button_write)

        # USTAWIENIA UKŁADU
        self.box_circuit.setLayout(self.layout_circuit)
        box_config.setLayout(layout_config)
        layout_main.addWidget(self.box_circuit)
        layout_main.addWidget(box_config)
        self.setLayout(layout_main)

    @pyqtSlot()
    def choose_file(self) -> None:
        """
        Wybranie pliku z danymi
        :return: None
        """
        file_name = QFileDialog.getOpenFileName(self, filter="*.pkl")[0]  # nazwa pliku
        circuit = load_data(file_name)
        self.parent.circuit_name = circuit.name
        self.parent.circuit_track_distance = circuit.track_dist
        self.parent.circuit_no_laps = circuit.no_laps
        self.parent.circuit_t_pit = circuit.t_pit
        self.parent.circuit_tires = circuit.tires
        
        self.layout_circuit.itemAt(0, QFormLayout.ItemRole.FieldRole).widget().setText(self.parent.circuit_name)
        self.layout_circuit.itemAt(1, QFormLayout.ItemRole.FieldRole).widget().setValue(self.parent.circuit_no_laps)
        self.layout_circuit.itemAt(2, QFormLayout.ItemRole.FieldRole).widget().setValue(self.parent.circuit_track_distance)
        self.layout_circuit.itemAt(3, QFormLayout.ItemRole.FieldRole).widget().setValue(self.parent.circuit_t_pit)
        for tire in circuit.tires:
            self.layout_circuit.itemAt(4, QFormLayout.ItemRole.FieldRole).layout().itemAt(0).widget().addItem(str(tire))

    @pyqtSlot()
    def add(self) -> None:
        params = [0, 0., 0., 0., 0., 0, 0, 0, 0, 0, 0]
        AddDialog(self, params).exec()
        tire = Tire(Compound(params[0]), params[5], params[1], params[2], params[3], params[4])
        for _ in range(params[6]):
            tire.lap_completed(Aggression.TIRES_MANAGING)
        for _ in range(params[7]):
            tire.lap_completed(Aggression.EASY)
        for _ in range(params[8]):
            tire.lap_completed(Aggression.NORMAL)
        for _ in range(params[9]):
            tire.lap_completed(Aggression.PUSH)
        for _ in range(params[10]):
            tire.lap_completed(Aggression.HARD_PUSH)
        self.parent.circuit_tires.append(tire)
        self.list_tires.addItem(str(tire))

    @pyqtSlot()
    def edit(self) -> None:
        self.list_tires.addItem("text")

    @pyqtSlot()
    def remove(self) -> None:
        current_row = self.list_tires.currentRow()
        if current_row >= 0:
            current_item = self.list_tires.takeItem(current_row)
            del current_item

    @pyqtSlot()
    def clear(self) -> None:
        self.list_tires.clear()

class AddDialog(QDialog):
    def __init__(self, parent: QWidget, params: List[Any]) -> None:
        super().__init__(parent)

        self.params = params
        self.setWindowTitle("Dodaj oponę")
        self.layout = QVBoxLayout()

        info_label = QLabel("Uzupełnij parametry opony dane wzorem v(n) = c - k * exp(n * b + d)")

        tire_layout = QFormLayout()
        compound_combo = QComboBox()
        compound_combo.addItems(["Miękka", "Pośrednia", "Twarda"])
        compound_combo.currentIndexChanged.connect(self.update_compund)
        tire_layout.addRow("Rodzaj mieszanki: ", compound_combo)
        spin_c = QDoubleSpinBox(self)
        spin_c.setValue(0.)
        spin_c.setDecimals(3)
        spin_c.setRange(-999, 999)
        spin_c.valueChanged.connect(self.update_c)
        tire_layout.addRow("Współczynnik c:", spin_c)
        spin_k = QDoubleSpinBox(self)
        spin_k.setValue(0.)
        spin_k.setDecimals(3)
        spin_k.setRange(-999, 999)
        spin_k.valueChanged.connect(self.update_k)
        tire_layout.addRow("Współczynnik k:", spin_k)
        spin_b = QDoubleSpinBox(self)
        spin_b.setValue(0.)
        spin_b.setDecimals(3)
        spin_b.setRange(-999, 999)
        spin_b.valueChanged.connect(self.update_b)
        tire_layout.addRow("Współczynnik b:", spin_b)
        spin_d = QDoubleSpinBox(self)
        spin_d.setValue(0.)
        spin_d.setDecimals(3)
        spin_d.setRange(-999, 999)
        spin_d.valueChanged.connect(self.update_d)
        tire_layout.addRow("Współczynnik d:", spin_d)
        spin_max_laps = QSpinBox(self)
        spin_max_laps.setValue(0)
        spin_max_laps.valueChanged.connect(self.update_max_laps)
        tire_layout.addRow("Maksymalna liczba okrążeń:", spin_max_laps)
        spin_a0 = QSpinBox(self)
        spin_a0.setValue(0)
        spin_a0.valueChanged.connect(self.update_a0)
        tire_layout.addRow("Przejechane okrążenia z agresywnością 0:", spin_a0)
        spin_a1 = QSpinBox(self)
        spin_a1.setValue(0)
        spin_a1.valueChanged.connect(self.update_a1)
        tire_layout.addRow("Przejechane okrążenia z agresywnością 1:", spin_a1)
        spin_a2 = QSpinBox(self)
        spin_a2.setValue(0)
        spin_a2.valueChanged.connect(self.update_a2)
        tire_layout.addRow("Przejechane okrążenia z agresywnością 2:", spin_a2)
        spin_a3 = QSpinBox(self)
        spin_a3.setValue(0)
        spin_a3.valueChanged.connect(self.update_a3)
        tire_layout.addRow("Przejechane okrążenia z agresywnością 3:", spin_a3)
        spin_a4 = QSpinBox(self)
        spin_a4.setValue(0)
        spin_a4.valueChanged.connect(self.update_a4)
        tire_layout.addRow("Przejechane okrążenia z agresywnością 4:", spin_a4)

        add_button = QPushButton("Dodaj")
        add_button.clicked.connect(self.accept)

        self.layout.addWidget(info_label)
        self.layout.addLayout(tire_layout)
        self.layout.addWidget(add_button)
        self.setLayout(self.layout)

    @pyqtSlot(int)
    def update_compund(self, compound: int) -> None:
        """
        Uaktualnienie mieszanki
        :param compund: (int) : mieszanka z ComboBox
        :return: None
        """
        self.params[0] = compound

    @pyqtSlot(float)
    def update_c(self, c: float) -> None:
        """
        Uaktualnienie współczynnika c
        :param c: (float) : współczynnik
        :return: None
        """
        self.params[1] = c

    @pyqtSlot(float)
    def update_k(self, k: float) -> None:
        """
        Uaktualnienie współczynnika c
        :param k: (float) : współczynnik
        :return: None
        """
        self.params[2] = k

    @pyqtSlot(float)
    def update_b(self, b: float) -> None:
        """
        Uaktualnienie współczynnika b
        :param b: (float) : współczynnik
        :return: None
        """
        self.params[3] = b

    @pyqtSlot(float)
    def update_d(self, d: float) -> None:
        """
        Uaktualnienie współczynnika d
        :param d: (float) : współczynnik
        :return: None
        """
        self.params[4] = d

    @pyqtSlot(int)
    def update_max_laps(self, max_laps: int) -> None:
        """
        Uaktualnienie maksymalnej liczby opkrążeń
        :param max_laps: (int) : liczba okrążeń
        :return: None
        """
        self.params[5] = max_laps

    @pyqtSlot(int)
    def update_a0(self, a0: int) -> None:
        """
        Uaktualnienie liczby okrążeń przejechanej z z agresywnością 0
        :param a0: (int) : liczba okrążeń
        :return: None
        """
        self.params[6] = a0

    @pyqtSlot(int)
    def update_a1(self, a1: int) -> None:
        """
        Uaktualnienie liczby okrążeń przejechanej z z agresywnością 1
        :param a1: (int) : liczba okrążeń
        :return: None
        """
        self.params[7] = a1

    @pyqtSlot(int)
    def update_a2(self, a2: int) -> None:
        """
        Uaktualnienie liczby okrążeń przejechanej z z agresywnością 2
        :param a2: (int) : liczba okrążeń
        :return: None
        """
        self.params[8] = a2

    @pyqtSlot(int)
    def update_a3(self, a3: int) -> None:
        """
        Uaktualnienie liczby okrążeń przejechanej z z agresywnością 3
        :param a3: (int) : liczba okrążeń
        :return: None
        """
        self.params[9] = a3

    @pyqtSlot(int)
    def update_a4(self, a4: int) -> None:
        """
        Uaktualnienie liczby okrążeń przejechanej z z agresywnością 4
        :param a4: (int) : liczba okrążeń
        :return: None
        """
        self.params[10] = a4

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
