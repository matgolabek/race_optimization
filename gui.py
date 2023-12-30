from data import *
import sys
from population import *
from typing import List, Any
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, \
    QFileDialog, QComboBox, QLineEdit, QGroupBox, QTabWidget, QLabel, QPushButton, QDialog, \
    QDoubleSpinBox, QSpinBox, QListWidget, QGridLayout, QRadioButton, QCheckBox
from PyQt6.QtCore import pyqtSlot, QPoint, Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPolygon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import matplotlib.pyplot as plt
import matplotlib
from ae import evolutionary_algorithm

matplotlib.use('TkAgg')


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
        self.population_size = 0
        self.selection_type = 99
        # self.is_elitist = False
        # self.elitist_size = 5
        self.parents_selected_num = 0
        self.cross_method = 99
        self.cross_probability = 0

        self.mutate_aggression = 0
        self.mutate_compound = 0
        self.mutate_pitstop = 0
        self.mutate_aggression_probability = 0
        self.mutate_compound_probability = 0
        self.mutate_pitstop_probability = 0

        # ROZWIĄZANIA
        self.time = 0
        self.total_iterations_num = 0
        self.best_individual = None
        self.best_iteration = 0
        self.best_individuals = []

        # USTAWIENIA OKNA

        self.resize(1200, 800)  # rozmiar
        self.setWindowTitle('Optymalizacja wyścigu')  # nazwa okna

        tabs = QTabWidget()  # zakładki Konfiguracja, Rozwiązanie, Wykres
        tabs.setTabPosition(QTabWidget.TabPosition.North)  # pozycja zakłedek
        tabs.setMovable(False)  # przemieszczanie zakładek

        tabs.addTab(Config(self), 'Konfiguracja')  # dodanie zakładki Konfiguracja
        tabs.addTab(Solution(self), 'Rozwiązanie')  # dodanie zakładki Arkusz
        tabs.addTab(Chart(self), 'Wykres')  # dodanie zakładek Wykres

        self.setCentralWidget(tabs)  # umieszczenie zakładek w oknie

        self.showMaximized()  # otwiera na pełnym ekranie


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
        button_read = QPushButton("Wczytaj dane z pliku")  # wczytywanie z pliku
        button_read.setFixedSize(200, 50)
        button_read.clicked.connect(self.choose_file)

        button_write = QPushButton("Zapisz wprowadzone dane")  # zapisywanie do pliku
        button_write.setFixedSize(200, 50)
        button_write.clicked.connect(self.save_data_to_file)

        # wybór liczby iteracji
        spin_iteration_number = QSpinBox(self)
        spin_iteration_number.setRange(1, 1000)
        label_iteration = QLabel("Liczba iteracji:")
        spin_iteration_number.valueChanged.connect(
            self.set_iteration_number)  # jeśli zmieni się wartość, to przekazywana jest do funkcji
        spin_iteration_number.setFixedSize(50, 20)

        # wybór wielkości populacji
        spin_population_size = QSpinBox(self)
        spin_population_size.setRange(10, 1000)
        label_population = QLabel("Wielkość populacji:")
        spin_population_size.valueChanged.connect(self.set_population_size)
        spin_population_size.setFixedSize(50, 20)

        # metody selekcji
        box_selection = QGroupBox("Selekcja")
        layout_selection = QVBoxLayout()
        radio_select1 = QRadioButton("Ruletka")
        radio_select2 = QRadioButton("Turniej")
        radio_select_all = [radio_select1, radio_select2]
        for button in radio_select_all:
            button.toggled.connect(lambda state, toggled_button=button: self.set_selection_method(toggled_button))
            layout_selection.addWidget(button)
        label_parents_num = QLabel("Jaki % populacji ma zostać rodzicami?")
        spin_parents_num = QSpinBox()
        spin_parents_num.setRange(0, 100)
        spin_parents_num.setFixedSize(50, 20)
        spin_parents_num.valueChanged.connect(self.set_percentage_to_be_seletcted)
        layout_selection.addWidget(label_parents_num)
        layout_selection.addWidget(spin_parents_num)

        """
        check_elitist = QCheckBox("Elitarna?")  # czy selekcja ma być elitarna? jak checkbox zaznaczony to przekaż liczbę osobników do zostawienia w next gen
        spin_elitist = QSpinBox()
        spin_elitist.setRange(5, 1000)
        spin_elitist.setFixedSize(50, 20)
        check_elitist.stateChanged.connect(lambda state, checkbox=check_elitist, val=spin_elitist.value(): self.set_elitist_param(checkbox, val))

        layout_selection.addWidget(check_elitist)
        layout_selection.addWidget(spin_elitist)
        """
        box_selection.setLayout(layout_selection)

        # wybór operatora krzyżowania + prawdopodobieństwo krzyżowania
        box_cross = QGroupBox("Operatory krzyżowania")
        layout_cross = QVBoxLayout()
        radio1 = QRadioButton("Jednopunktowe środek")
        radio2 = QRadioButton("Jednopunktowe losowo")
        radio3 = QRadioButton("Przed pitstopem")
        radio4 = QRadioButton("Tylko agresja")
        radio5 = QRadioButton("Dwupunktowe losowo")
        radio_all = [radio1, radio2, radio3, radio4, radio5]
        for button in radio_all:
            button.toggled.connect(lambda state, toggled_button=button: self.set_cross_method(toggled_button))
            layout_cross.addWidget(button)

        spin_cross_probability = QSpinBox()
        spin_cross_probability.setRange(0, 100)
        label_cross_probability = QLabel("Z prawdopodobieństwem [%]:")
        spin_cross_probability.valueChanged.connect(self.set_cross_probability)
        spin_cross_probability.setFixedSize(50, 20)
        layout_cross.addWidget(label_cross_probability)
        layout_cross.addWidget(spin_cross_probability)
        box_cross.setLayout(layout_cross)

        # analogicznie wybór operatora mutacji
        box_mutate = QGroupBox("Operatory mutacji")
        layout_mutate = QVBoxLayout()
        check1_mutate = QCheckBox("Agresja")
        label1_mutate = QLabel("Z prawdopodobieństwem [%]:")
        spin1_mutate = QSpinBox()
        spin1_mutate.setRange(0, 100)
        spin1_mutate.setFixedSize(50, 20)
        check2_mutate = QCheckBox("Mieszanka")
        label2_mutate = QLabel("Z prawdopodobieństwem [%]:")
        spin2_mutate = QSpinBox()
        spin2_mutate.setRange(0, 100)
        spin2_mutate.setFixedSize(50, 20)
        check3_mutate = QCheckBox("Pitstop")
        label3_mutate = QLabel("Z prawdopodobieństwem [%]:")
        spin3_mutate = QSpinBox()
        spin3_mutate.setRange(0, 100)
        spin3_mutate.setFixedSize(50, 20)

        # jeśli checkbox jest zaznaczony lub zmieniona jest wartość prawdopodobieństwa
        check1_mutate.stateChanged.connect(
            lambda state, checkbox=check1_mutate, val=spin1_mutate.value(): self.set_mutate_aggression_probability(
                checkbox, val))
        spin1_mutate.valueChanged.connect(
            lambda state, checkbox=check1_mutate, val=spin1_mutate.value(): self.set_mutate_aggression_probability(
                checkbox, val))
        check2_mutate.stateChanged.connect(
            lambda state, checkbox=check2_mutate, val=spin2_mutate.value(): self.set_mutate_compound_probability(
                checkbox, val))
        spin2_mutate.valueChanged.connect(
            lambda state, checkbox=check2_mutate, val=spin2_mutate.value(): self.set_mutate_compound_probability(
                checkbox, val))
        check3_mutate.stateChanged.connect(
            lambda state, checkbox=check3_mutate, val=spin3_mutate.value(): self.set_mutate_pitstop_probability(
                checkbox, val))
        spin3_mutate.valueChanged.connect(
            lambda state, checkbox=check3_mutate, val=spin3_mutate.value(): self.set_mutate_pitstop_probability(
                checkbox, val))

        layout_mutate.addWidget(check1_mutate)
        layout_mutate.addWidget(label1_mutate)
        layout_mutate.addWidget(spin1_mutate)
        layout_mutate.addWidget(check2_mutate)
        layout_mutate.addWidget(label2_mutate)
        layout_mutate.addWidget(spin2_mutate)
        layout_mutate.addWidget(check3_mutate)
        layout_mutate.addWidget(label3_mutate)
        layout_mutate.addWidget(spin3_mutate)
        box_mutate.setLayout(layout_mutate)

        button_start_alg = QPushButton("Algorytm ewolucyjny - start")  # przycisk rozpoczynający algorytm
        button_start_alg.setFixedSize(200, 50)
        button_start_alg.clicked.connect(self.start_ae)

        layout_config.addWidget(button_read)  # dodanie tych wszystkich rzeczy do layoutu
        layout_config.addWidget(button_write)
        layout_config.addWidget(label_iteration)
        layout_config.addWidget(spin_iteration_number)
        layout_config.addWidget(label_population)
        layout_config.addWidget(spin_population_size)
        layout_config.addWidget(box_selection)
        layout_config.addWidget(box_cross)
        layout_config.addWidget(box_mutate)
        layout_config.addWidget(button_start_alg)

        layout_config.addStretch()  # wszystko się wyświetla jedno pod drugim
        layout_config.setSpacing(10)

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
        self.layout_circuit.itemAt(2, QFormLayout.ItemRole.FieldRole).widget().setValue(
            self.parent.circuit_track_distance)
        self.layout_circuit.itemAt(3, QFormLayout.ItemRole.FieldRole).widget().setValue(self.parent.circuit_t_pit)
        self.layout_circuit.itemAt(4, QFormLayout.ItemRole.FieldRole).layout().itemAt(0).widget().clear()
        for tire in circuit.tires:
            self.layout_circuit.itemAt(4, QFormLayout.ItemRole.FieldRole).layout().itemAt(0).widget().addItem(str(tire))

    def save_data_to_file(self) -> None:
        """
        Zapisywanie danych wprowadzonych ręcznie do pliku pkl
        :return: None
        """
        new_circuit = Circuit(self.parent.circuit_name, self.parent.circuit_track_distance, self.parent.circuit_no_laps,
                              self.parent.circuit_t_pit, self.parent.circuit_tires)
        write_data(new_circuit)

    def set_iteration_number(self, value_from_spinbox) -> None:
        """
        Wprowadzona przez użytkownika liczba iteracji zapisuje się w zmiennej
        (wywołuje się, gdy zmieni się wartość w spinboxie)
        :return: None
        """
        self.parent.iterations = value_from_spinbox

    def set_population_size(self, value_from_spinbox) -> None:
        """
        Analogicznie do powyższej ustawia wielkość populacji
        :param value_from_spinbox:
        :return: nic
        """
        self.parent.population_size = value_from_spinbox

    def set_selection_method(self, toggled_button) -> None:
        """
        Wybór metody selekcji
        :param toggled_button: zaznaczony radio button
        :return: Nic
        """
        if toggled_button.text() == "Ruletka":
            self.parent.selection_type = 0
        elif toggled_button.text() == "Turniej":
            self.parent.selection_type = 1

    def set_percentage_to_be_seletcted(self, value_from_spinbox) -> None:
        """
        Ile procent osobników ma zostać rodzicami?
        """
        self.parent.parents_selected_num = value_from_spinbox / 100

    def set_cross_method(self, toggled_button) -> None:
        """
        Wybór operatora krzyżowania
        :return: NiC
        """
        if toggled_button.text() == "Jednopunktowe środek":
            self.parent.cross_method = 0
        elif toggled_button.text() == "Jednopunktowe losowo":
            self.parent.cross_method = 1
        elif toggled_button.text() == "Przed pitstopem":
            self.parent.cross_method = 2
        elif toggled_button.text() == "Tylko agresja":
            self.parent.cross_method = 3
        elif toggled_button.text() == "Dwupunktowe losowo":
            self.parent.cross_method = 4

    def set_cross_probability(self, value_from_spinbox):
        """
        Ustawienie p. krzyżowania
        :return: NIC
        """
        self.parent.cross_probability = value_from_spinbox / 100

    def set_mutate_aggression_probability(self, checkbox, value):
        """
        Mutacja agresji
        :param checkbox:
        :param value:
        :return:
        """
        if checkbox.checkState():
            self.parent.mutate_aggression = 1  # jeśli checkbox zaznaczony
            self.parent.mutate_aggression_probability = value / 100  # prawodopodobieństwo zmieni się tylko jeśli zaznaczony jest checkbox
        else:
            self.parent.mutate_aggression = 0

    def set_mutate_compound_probability(self, checkbox, value):
        """
        Mutacja agresji
        :param checkbox:
        :param value:
        :return:
        """
        if checkbox.checkState():
            self.parent.mutate_compound = 1
            self.parent.mutate_compound_probability = value / 100
        else:
            self.parent.mutate_compound = 0

    def set_mutate_pitstop_probability(self, checkbox, value):
        """
        Mutacja agresji
        :param checkbox:
        :param value:
        :return:
        """
        if checkbox.checkState():
            self.parent.mutate_pitstop = 1
            self.parent.mutate_pitstop_probability = value / 100
        else:
            self.parent.mutate_pitstop = 0

    def start_ae(self):
        """
        Przekazanie danych do algorytmu i liczenie
        """
        new_circuit = Circuit(self.parent.circuit_name, self.parent.circuit_track_distance, self.parent.circuit_no_laps,
                              self.parent.circuit_t_pit, self.parent.circuit_tires)

        solution = evolutionary_algorithm(self.parent.population_size, new_circuit, self.parent.iterations,
                                          self.parent.parents_selected_num, self.parent.selection_type,
                                          self.parent.cross_method, self.parent.cross_probability,
                                          self.parent.mutate_aggression,
                                          self.parent.mutate_aggression_probability, self.parent.mutate_compound,
                                          self.parent.mutate_compound_probability, self.parent.mutate_pitstop,
                                          self.parent.mutate_pitstop_probability)
        self.parent.time = solution[0]
        self.parent.total_iterations_num = solution[1]
        self.parent.best_individual = solution[2]
        self.parent.best_iteration = solution[3]
        self.parent.best_individuals = solution[4]

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
        current_row = self.list_tires.currentRow()
        if current_row >= 0:
            current_item = self.list_tires.takeItem(current_row)
            del current_item
            params = [0, 0., 0., 0., 0., 0, 0, 0, 0, 0, 0]
            AddDialog(self, params, True).exec()
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
            self.parent.circuit_tires[current_row] = tire
            self.list_tires.insertItem(current_row, str(tire))

    @pyqtSlot()
    def remove(self) -> None:
        current_row = self.list_tires.currentRow()
        if current_row >= 0:
            current_item = self.list_tires.takeItem(current_row)
            self.parent.circuit_tires.pop(current_row)
            del current_item

    @pyqtSlot()
    def clear(self) -> None:
        self.parent.circuit_tires = []
        self.list_tires.clear()


class Solution(QWidget):

    def __init__(self, parent: MainWindow):
        """
        Zakładka z rozwiązaniem
        :param parent: (QMainWindow) : okno rodzic
        """
        super(Solution, self).__init__()

        self.parent = parent  # wskaźnik na rodzica

        self.label = QLabel()
        self.canvas = QPixmap(1900, 900)
        self.canvas.fill(QColor("white"))
        self.label.setPixmap(self.canvas)

        self.button = QPushButton("Pokaż rozwiązanie")  # przycisk na rysowanie wykresu
        self.button.clicked.connect(self.draw_solution)

        layout_main = QVBoxLayout()  # układ główny

        # USTAWIENIA UKŁADU
        layout_main.addWidget(self.label)
        layout_main.addWidget(self.button)
        self.setLayout(layout_main)

    def draw_solution(self) -> None:
        """
        Rysowanie odpowiedzi
        :return: None
        """
        pits = [10, 30, 40]
        with QPainter(self.canvas) as painter:
            painter_font = QFont()
            painter_font.setPixelSize(20)
            painter.setFont(painter_font)
            h = 50
            w = 50
            for n in range(self.parent.circuit_no_laps):
                if w > 1750:
                    w = 50
                    h += 200
                if n in pits:
                    triangle = QPolygon()
                    triangle << QPoint(w + 100, h) << QPoint(w + 80, h - 35) << QPoint(w + 120, h - 35)
                    painter.drawConvexPolygon(triangle)
                    painter.drawText(w + 95, h - 15, "P")
                painter.drawRect(w, h, 100, 100)
                painter.fillRect(w + 1, h + 1, 99, 99, QColor(random.choice(["yellow", "red", "light grey"])))
                if n < 9:
                    painter.drawText(w + 45, h + 60, str(n + 1))
                else:
                    painter.drawText(w + 40, h + 60, str(n + 1))
                w += 100
        self.label.setPixmap(self.canvas)


class Chart(QWidget):

    def __init__(self, parent: MainWindow):
        """
        Zakładka z wykresem wartości funkcji celu od iteracji
        :param parent: (QMainWindow) : okno rodzic
        """
        super(Chart, self).__init__()

        self.parent = parent  # wskaźnik na rodzica

        self.figure = plt.figure()  # wykres
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.button = QPushButton("Narysuj wykres")  # przycisk na rysowanie wykresu
        self.button.clicked.connect(self.plot_graph)

        layout = QVBoxLayout()  # układ
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    @pyqtSlot()
    def plot_graph(self) -> None:
        """
        Rysowanie wykresu
        :return: None
        """
        self.figure.clear()
        ax = self.figure.add_subplot()
        ax.clear()
        ax.step([1, 2, 3, 4, 5, 6], [10, 20, 30, 40, 20, 10])
        ax.set(xlabel="Liczba iteracji", ylabel="Wartość funkcji celu",
               title="Wartość funkcji celu od liczby iteracji", xlim=[1, self.parent.circuit_no_laps])
        self.canvas.draw()


# DODANIE OPONY DO ZAKŁADKI CONFIG

class AddDialog(QDialog):
    def __init__(self, parent: QWidget, params: List[Any], is_edit: bool = False) -> None:
        super().__init__(parent)

        self.params = params
        if not is_edit:
            self.setWindowTitle("Dodaj oponę")
        else:
            self.setWindowTitle("Edytuj oponę")
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

        if not is_edit:
            add_button = QPushButton("Dodaj")
        else:
            add_button = QPushButton("Edytuj")
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
