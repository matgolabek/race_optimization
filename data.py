from typing import List
from enum import Enum
from math import exp
import pickle


class Pit(Enum):  # Rodzaje wykonania pit stopu
    NO = 0
    YES = 1


class Compound(Enum):  # Rodzaje mieszanki
    SOFT = 1
    MEDIUM = 2
    HARD = 3


class Aggression(Enum):  # Rodzaj agresywności
    TIRES_MANAGING = 1
    EASY = 2
    NORMAL = 3
    PUSH = 4
    HARD_PUSH = 5


class Tire:
    def __init__(self, compound: Compound, max_laps: int, c: float, k: float, b: float, d: float):
        """
        Opona
        :param compound: (Compound) : rodzaj mieszanki
        :param max_laps: (int) : maksymalna liczba okrążeń
        :param c: (float) : współczynnik c we wzorze v(n) = c - k * exp(n * b + d)
        :param k: (float) : współczynnik k we wzorze v(n) = c - k * exp(n * b + d)
        :param b: (float) : współczynnik b we wzorze v(n) = c - k * exp(n * b + d)
        :param d: (float) : współczynnik d we wzorze v(n) = c - k * exp(n * b + d)
        """
        self.compound = compound   # mieszanka
        self.max_laps = max_laps  # maksymalna liczba okrążeń
        self.c = c
        self.k = k
        self.b = b
        self.d = d
        self.n = 0  # liczba pokonanych okrążeń
        self.aggression = []  # agresja na okrążeniu

    def __repr__(self) -> str:
        return '{} laps on {} tires ({})\n'.format(self.n, self.compound.name, self.aggression)

    def lap_completed(self, aggression: Aggression) -> float:
        """
        Metoda zapisująca wykonane okrążenie opony z daną agresywnością
        :param aggression: (Aggression) : współczynnik agresywności na okrążeniu
        :return: (float) : średnia szybkość jazdy na tym okrążeniu [m/s]
        """
        self.n += 1
        self.aggression.append(aggression.name)
        c = self.c
        k = self.k
        b = self.b
        d = self.d
        if aggression == Aggression.TIRES_MANAGING:
            c = self.c * 0.95
            k = self.k * 0.95
            b = self.b * 0.9
            d = self.d * 0.9
            self.max_laps += self.max_laps * 0.1
        elif aggression == Aggression.EASY:
            c = self.c * 0.975
            k = self.k * 0.975
            b = self.b * 0.95
            d = self.d * 0.95
            self.max_laps += self.max_laps * 0.05
        elif aggression == Aggression.PUSH:
            c = self.c * 1.025
            k = self.k * 1.025
            b = self.b * 1.05
            d = self.d * 1.05
            self.max_laps -= self.max_laps * 0.05
        elif aggression == Aggression.HARD_PUSH:
            c = self.c * 1.05
            k = self.k * 1.05
            b = self.b * 1.1
            d = self.d * 1.1
            self.max_laps -= self.max_laps * 0.1
        if self.n < self.max_laps:
            return c - k * exp(self.n * b + d)
        else:
            return 0.


class Circuit:
    def __init__(self, name: str, track_dist: int, no_laps: int, t_pit: float, tires: List[Tire]):
        """
        Tor
        :param name: (str) : nazwa toru (miasto)
        :param track_dist: (int) : długość toru
        :param no_laps: (int) : liczba okrążeń
        :param t_pit: (float) : czas wykonywania pit stopu
        :param tires: (List[Tire]) : lista opon dostępnych na wyścig
        """
        self.name = name
        self.track_dist = track_dist
        self.no_laps = no_laps
        self.t_pit = t_pit
        self.tires = tires

    def __repr__(self) -> str:
        return 'Name: {}\n'.format(self.name) + 'Track distance: {} m\n'.format(self.track_dist)\
               + 'No. laps: {}\n'.format(self.no_laps) + 'Pit stop time: {} s\n'.format(self.t_pit)\
               + 'Available tires: {}'.format(self.tires)


def write_data(circuit: Circuit) -> None:
    """
    Funkcja zapisująca tor na dysku (w folderze Circuits)
    :param circuit: (Circuit) : Tor
    :return: None
    """
    with open('Circuits/{}.pkl'.format(circuit.name), 'wb') as file:
        pickle.dump(circuit, file)


def load_data(file_name: str) -> Circuit:
    """
    Funkcja odczytująca tor (dane do obliczeń) z pliku
    :param file_name: (str) : nazwa pliku
    :return: (Circuit) : Tor
    """
    with open(file_name, 'rb') as file:
        return pickle.load(file)
