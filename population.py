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

    def __init__(self,list_of_laps,c:Circuit):
        self.list_of_laps = list_of_laps
        self.size = len(list_of_laps)
        self.fitness = time_function(list_of_laps,c)   #Osobnik, bo to jest wyliczane pole klasy Osobnik, więc Osobnik jeszcze jakby nie istnieje dopóki nie ma wyliczonego przystosowania!!!!

    def update_fitness(self,c:Circuit):
        self.fitness = time_function(self.list_of_laps,c)

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

    def __init__(self, individuals: List[Individual],c: Circuit):

        self.individuals = individuals   # lista osobników
        self.picked_parents = []    # lista rodziców wybieranych z osobników
        self.new_individuals = []   # lista nowych osobników po krzyżowaniu i mutacji; z niej stworzona będzie nowa populacja
        self.circuit = c
        self.size = len(individuals)

    def start_population(self,size) -> None:
        """
        :param size (int) : rozmiar populacji
        :param infividuals (List[Inddividuals]) : rodzice przekazani z poprzedniej populacji
        """
        N = self.circuit.no_laps
        # tworzenie losowych osobników
        # size*N*(p, A, o) -  size razy N krotek
        for i in range(size):
            list_of_laps = []     # każdy osobnik to N-elementowa lista krotek
            for lap in range(N):    # N okrążeń w każdym osobniku
                pit = random.choices(list(Pit), weights=[0.9, 0.1])[0]  # PIT=YES z prawdopodobieństwem X
                aggression = random.choice(list(Aggression)) # agresja wybierana jest losowo      
                if lap==0 or pit==Pit.YES:
                    compound = random.choice(list(Compound))   # rodzaj mieszanki ustalany, gdy wystąpi pitstop i nie zmienia sie do kolejnego pitstopu  
                partial_ind = PartialIndividual(pit, aggression, compound)  # okrążenie (1/N-ta część osobnika)
                list_of_laps.append(partial_ind)    # wszystkie okrążenia zbierane do listy
            individual = Individual(list_of_laps,copy.deepcopy(self.circuit))  # po wypełnieniu listy okrążeniami tworzony jest nowy osobnik
            self.individuals.append(individual)  # na koniec powstały osobnik jest dodawany do listy wszystkich osobników
            self.size = len(self.individuals)

    def shuffle_population(self):

        # połącz new_individuals z individuals
        # nw czy to będzie ok, ale żeby np. jak populacja bazowa ma rozmiar x (ind) a new_ind ma rozmiar y, to żeby z ind dobrać k najlepszych osobników, żeby y+k=x

        for i in range(self.size-len(self.new_individuals)):
            parrent = min(self.individuals, key = lambda x: x.fitness)
            self.individuals.pop(self.individuals.index(parrent))
            self.new_individuals.append(parrent)     # jeśli to doprowadzi do super osobnikow to ofc dodac to jakas losowosc
            