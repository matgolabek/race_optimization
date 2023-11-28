import data
import random
import Funkcja_celu
# from typing import Self nie działa u mnie z jakiegoś powodu


# [p, A, o]
class PartialIndividual:

    def __init__(self, pit: data.Pit, aggresssion: data.Aggression, compound: data.Compound):
        self.pit = pit
        self.aggression = aggresssion
        self.compound = compound

    def __repr__(self):
        return "[p = " + str(self.pit) + ", A = " + str(self.aggression) + ", o = " + str(self.compound) + "]"


# N * [p, A, o]
class Individual:

    def __init__(self, N, list_of_laps):
        self.size = N
        self.list_of_laps = list_of_laps
        self.fitness = Funkcja_celu.time_function(# arg ??? jaki tu t_stop????)

    def __repr__(self):
        s = ""
        for i in range(self.size):
            s += str(i)
            s += ": "
            s += str(self.list_of_laps[i])
            s += "\n"
        return s


# populacja startowa
class StartPopulation:

    def __init__(self, size: int, N: int):

        self.size = size    # rozmiar populacji
        self.individuals = []   # lista osobników
        self.picked_parents = []    # lista rodziców wybieranych z osobników

        self.new_individuals = []   # lista nowych osobników po krzyżowaniu i mutacji, z niej stworzona będzie nowa populacja

        # tworzenie losowych osobników
        # size*N*(p, A, o) -  size razy N krotek
        for i in range(size):
            list_of_laps = []     # każdy osobnik to N-elementowa lista krotek
            for lap in range(N):    # N okrążeń w każdym osobniku
                pit = random.choices(list(data.Pit), weights=[0.1, 0.9])[0]  # PIT=YES z p=0.9
                aggression = random.choice(list(data.Aggression))
                compound = random.choice(list(data.Compound))   # agresja oraz rodzaj mieszanki są wybierane po prostu losowo
                partial_ind = PartialIndividual(pit, aggression, compound)  # okrążenie (1/N-ta część osobnika)
                list_of_laps.append(partial_ind)    # wszystkie okrążenia zbierane do listy
            individual = Individual(N, list_of_laps)  # po wypełnieniu listy okrążeniami tworzony jest nowy osobnik
            self.individuals.append(individual)  # na koniec powstały osobnik jest dodawany do listy wszystkich osobników

    def pick_parents(self, m: int, n: int):
        # m - liczba pozbiorów
        # n - liczba osobników w każdym podzbiorze
        # 1. obliczenie funkcji celu dla każdego osobnika
        # 2. wyznaczenie m podzbiorów, n-elementowych
        # 3. z każdego pozbioru wybór 1 elementu i wrzucenie go do picked_parents
        pass

    def cross(self):
        pass

    def mutate(self):
        pass


# każda kolejna populacja (osobniki nie są już generowane losowo)
class NextPopulation:

    def __init__(self, size, individuals):

        self.size = size
        self.individuals = individuals
        self.picked_parents = []

        self.new_individuals = []

    def pick_parents(self, m: int, n: int):
        pass

    def cross(self):
        pass

    def mutate(self):
        pass
