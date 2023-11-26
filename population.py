import data
import random


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
            individual = []     # każdy osobnik to N-elementowa lista krotek
            for lap in range(N):    # N okrążeń w każdym osobniku
                pit = random.choices(list(data.Pit), weights=[0.1, 0.9])[0]  # PIT=YES z p=0.9
                aggression = random.choice(list(data.Aggression))
                compound = random.choice(list(data.Compound))   # agresja oraz rodzaj mieszanki są wybierane po prostu losowo
                individual.append((pit, aggression, compound))
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
