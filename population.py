import random
from objective_function import *
import copy


# [p, A, o]
class PartialIndividual:    # Gen

    def __init__(self, pit: Pit, aggresssion: Aggression, compound: Compound):
        self.pit = pit
        self.aggression = aggresssion
        self.compound = compound

    def __repr__(self):
        return "[p = " + str(self.pit) + ", A = " + str(self.aggression) + ", o = " + str(self.compound) + "]"


# N * [p, A, o]
class Individual:

    def __init__(self, N, list_of_laps,c:Circuit):
        self.size = N
        self.list_of_laps = list_of_laps
        self.fitness = time_function(list_of_laps,c)   # funckja celu musi mieć argumenty (N, list_of laps) a Osobnik, bo to jest wyliczane pole klasy Osobnik, więc Osobnik jeszcze jakby nie istnieje dopóki nie ma wyliczonego przystosowania!!!!

    def __repr__(self):
        s = ""
        for i in range(self.size):
            s += str(i)
            s += ": "
            s += str(self.list_of_laps[i])
            s += "\n"
        s += str(self.fitness)
        s += " [min] \n"
        return s


# populacja startowa
class NextPopulation:

    def __init__(self, individuals: List[Individual]):

        self.individuals = individuals   # lista osobników
        self.picked_parents = []    # lista rodziców wybieranych z osobników
        self.new_individuals = []   # lista nowych osobników po krzyżowaniu i mutacji; z niej stworzona będzie nowa populacja

    def start_population(self,size: int,c: Circuit) -> None:
        """
        :param size (int) : rozmiar populacji
        :param infividuals (List[Inddividuals]) : rodzice przekazani z poprzedniej populacji
        """
        N = c.no_laps
        # tworzenie losowych osobników
        # size*N*(p, A, o) -  size razy N krotek
        for i in range(size):
            list_of_laps = []     # każdy osobnik to N-elementowa lista krotek
            for lap in range(N):    # N okrążeń w każdym osobniku
                pit = random.choices(list(Pit), weights=[0.92, 0.08])[0]  # PIT=YES z prawdopodobieństwem 8%
                aggression = random.choice(list(Aggression)) # agresja wybierana jest losowo      
                if lap==0 or pit==Pit.YES:
                    compound = random.choice(list(Compound))   # rodzaj mieszanki ustalany, gdy wystąpi pitstop i nie zmienia sie do kolejnego pitstopu  
                partial_ind = PartialIndividual(pit, aggression, compound)  # okrążenie (1/N-ta część osobnika)
                list_of_laps.append(partial_ind)    # wszystkie okrążenia zbierane do listy
            individual = Individual(N, list_of_laps,copy.deepcopy(c))  # po wypełnieniu listy okrążeniami tworzony jest nowy osobnik
            self.individuals.append(individual)  # na koniec powstały osobnik jest dodawany do listy wszystkich osobników

    def pick_parents(self, m: int, n: int, selection) -> None:     # ważne, żeby m było parzystą liczbą
        """
        :param m (int) : liczba pozbiorów
        :param n (int) : liczba osobników w każdym podzbiorze
        :param selection ()- rodzaj wybranej selekcji
        1. obliczenie funkcji celu dla każdego osobnika - to jest już pole klasy Individual.fitness
        2. wyznaczenie m podzbiorów, n-elementowych
        """ 
        subsets = []
        for _ in range(m):
            subsets.append(random.sample(self.individuals, n))
        # 3. z każdego pozbioru wybór 1 elementu i wrzucenie go do picked_parents
        for subset in subsets:
            self.picked_parents.append(max(subset, key = lambda x: x.fitness))    # wybierz najlepiej przystosowanego
        # UWAGA - kod nie uwzględnia tego czy osobnik już wcześniej został wybrany do podzbioru
        # więc może dojść do przypadku, że z podzbioru 1 i 2 zostanie wybrany ten sam rodzic

    def cross(self):

        while self.picked_parents:

            # losowy wybrani rodzice z listy
            inx = random.randint(0, len(self.picked_parents) - 1)
            parent1 = self.picked_parents.pop(inx)
            inx = random.randint(0, len(self.picked_parents) - 1)
            parent2 = self.picked_parents.pop(0)

            # krzyżowanie
            midpoint = parent1.size // 2
            child1 = parent1[:midpoint] + parent2[midpoint:]
            child2 = parent2[:midpoint] + parent1[midpoint:]

            # dzieci idą do new_ind
            self.new_individuals.append(child1)
            self.new_individuals.append(child2)

    def mutate(self,mutation_prob):

        for individual in self.new_individuals:
            for gene in individual:
                change = random.choices([False, True], [0.97, 0.03])[0]     # dla każdego genu oblicz czy ma wystąpić mutacja
                if change:
                    # jak tak to zmień agresję - na numer inny niż obecny gene.aggression
                    aggressions = list(Aggression)
                    aggressions.remove(gene.aggression)
                    new_aggression = random.choices(aggressions, [0.25, 0.25, 0.25, 0.25])[0]
                    gene.aggression = new_aggression

    def shuffle_population(self):

        # połącz new_individuals z individuals
        # nw czy to będzie ok, ale żeby np. jak populacja bazowa ma rozmiar x (ind) a new_ind ma rozmiar y, to żeby z ind dobrać k najlepszych osobników, żeby y+k=x

        while len(self.new_individuals != self.individuals):
            self.new_individuals.append(max(self.individuals, lambda x: x.fitness))     # jeśli to doprowadzi do super osobnikow to ofc dodac to jakas losowosc
