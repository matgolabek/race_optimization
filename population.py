import data
import random
import Funkcja_celu
import main


# [p, A, o]
class PartialIndividual:    # Gen

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
        self.fitness = Funkcja_celu.time_function(main.j)   # funckja celu musi mieć argumenty (N, list_of laps) a Osobnik, bo to jest wyliczane pole klasy Osobnik, więc Osobnik jeszcze jakby nie istnieje dopóki nie ma wyliczonego przystosowania!!!!

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

    def __init__(self, size: int, c: data.Circuit):

        N = c.no_laps
        self.size = size    # rozmiar populacji
        self.individuals = []   # lista osobników
        self.picked_parents = []    # lista rodziców wybieranych z osobników

        self.new_individuals = []   # lista nowych osobników; po krzyżowaniu i mutacji, z niej stworzona będzie nowa populacja

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
        # 1. obliczenie funkcji celu dla każdego osobnika - to jest już pole klasy Individual.fitness
        # 2. wyznaczenie m podzbiorów, n-elementowych
        subsets = []
        for _ in range(m):
            subsets.append(random.sample(self.individuals, n))
        # 3. z każdego pozbioru wybór 1 elementu i wrzucenie go do picked_parents
        for subset in subsets:
            self.picked_parents.append(max(subset, lambda x: x.fitness))    # wybierz najlepiej przystosowanego
        # UWAGA - kod nie uwzględnia tego czy osobnik już wcześniej został wybrany do podzbioru
        # więc może dojść do przypadku, że z podzbioru 1 i 2 zostanie wybrany ten sam rodzic

    def cross(self):
        # tutaj z picked_parents robi się new_individuals tylko jeszcze nw jak
        self.picked_parents = self.new_individuals

    def mutate(self):

        for individual in self.new_individuals:
            for gene in individual:
                change = random.choices([False, True], [0.97, 0.03])[0]     # dla każdego genu oblicz czy ma wystąpić mutacja
                if change:
                    # jak tak to zmień agresję - na numer inny niż obecny gene.aggression
                    aggressions = list(data.Aggression)
                    aggressions.remove(gene.aggression)
                    new_aggression = random.choices(aggressions, [0.25, 0.25, 0.25, 0.25])[0]
                    gene.aggression = new_aggression



# każda kolejna populacja (osobniki nie są już generowane losowo)

class NextPopulation:

    def __init__(self, individuals):

        self.individuals = individuals
        self.picked_parents = []

        self.new_individuals = []

    def pick_parents(self, m: int, n: int):

        subsets = []
        for _ in range(m):
            subsets.append(random.sample(self.individuals, n))
        for subset in subsets:
            self.picked_parents.append(max(subset, lambda x: x.fitness))

    def cross(self):
        pass

    def mutate(self):

        for individual in self.new_individuals:
            for gene in individual:
                change = random.choices([False, True], [0.97, 0.03])[0]     # dla każdego genu oblicz czy ma wystąpić mutacja
                if change:
                    # jak tak to zmień agresję - na numer inny niż obecny gene.aggression
                    aggressions = list(data.Aggression)
                    aggressions.remove(gene.aggression)
                    new_aggression = random.choices(aggressions, [0.25, 0.25, 0.25, 0.25])[0]
                    gene.aggression = new_aggression
