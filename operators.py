import random
from data import *
from population import NextPopulation,Individual
from typing import Union


def mutate_aggression(population: NextPopulation, probability: float = 0.03) -> None:
    """
    Mutacja tylko agresji z zadanym prawdopodobieństwem (domyślnie 0.05)
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :param probability: (float) : prawdopodobieństwo wystąpienia mutacji
    :return: None
    """
    if probability <= 0 or probability >= 1:
        probability = 0.05
    for individual in population.new_individuals:
        for gene in individual:
            change = random.choices([False, True], [1 - probability, probability])[0]
            if change:
                aggressions = list(Aggression)
                aggressions.remove(gene.aggression)
                new_aggression = random.choices(aggressions, [0.25, 0.25, 0.25, 0.25])[0]
                gene.aggression = new_aggression


def mutate_pit(population: NextPopulation, probability: float = 0.05) -> None:
    """
    Mutacja wykonania pit stopu z zadanym prawdpopodbieństwem (domyślnie 0.03)
    :param probability: (float) : prawdopodobieństwo wystąpienia mutacji
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :return: None
    """
    if probability <= 0 or probability >= 1:
        probability = 0.05
    for individual in population.new_individuals:
        for gene in individual:
            change = random.choices([False, True], [1 - probability, probability])[0]
            if change:
                if gene.pit == Pit.NO:
                    gene.pit = Pit.YES
                else:
                    gene.pit = Pit.NO


def mutate_compound(population: NextPopulation, probability: float = 0.05) -> None:
    """
    Mutacja rodzaju meszanki stopu z zadanym prawdpopodbieństwem (domyślnie 0.03)
    :param probability: (float) : prawdopodobieństwo wystąpienia mutacji
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :return: None
    """
    if probability <= 0 or probability >= 1:
        probability = 0.05
    for individual in population.new_individuals:
        for gene in individual:
            change = random.choices([False, True], [1 - probability, probability])[0]
            if change:
                compounds = list(Compound)
                compounds.remove(gene.compound)
                gene.compound = random.choices(compounds, [0.5, 0.5])[0]


def cross(population: NextPopulation, random_division_point: bool = False) -> None:
    """
    Krzyżowanie z domyślnym punktem podziału w środku osobnika lub w losowo wybranym
    :param random_division_point: (bool) : czy losować punkt podziału do krzyżowania
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :return: None
    """
    while population.picked_parents:
        inx = random.randint(0, len(population.picked_parents) - 1)
        parent1 = population.picked_parents.pop(inx)
        inx = random.randint(0, len(population.picked_parents) - 1) #### TU NIE WIEM O CO CHODZI
        parent2 = population.picked_parents.pop(inx)  #### ZMIENIŁEM POP(0) NA POP(INX)

        if random_division_point:
            midpoint = int(parent1.size * random.random())
        else:
            midpoint = parent1.size // 2

        child1 = parent1[:midpoint] + parent2[midpoint:]
        child2 = parent2[:midpoint] + parent1[midpoint:]

        population.new_individuals.append(child1)
        population.new_individuals.append(child2)


def cross_before_pit(population: NextPopulation, no_pit: int = 1, best_first: bool = False) -> None:
    """
    Krzyżowanie przed zadanym pit stopem losowego osobnika lub lepszego, gdy nie znajdzie pit sotpu to wylosuje punkt krzyżowania
    :param best_first: (bool) : krzyżowanie przed pierwszym pit stopem lepszego z rodziców
    :param no_pit: (int) : nr pit stopu przed którym ma wystąpić krzyżowanie
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :return: None
    """
    while population.picked_parents:
        inx = random.randint(0, len(population.picked_parents) - 1)
        parent1 = population.picked_parents.pop(inx)
        inx = random.randint(0, len(population.picked_parents) - 1) #### TU NIE WIEM O CO CHODZI
        parent2 = population.picked_parents.pop(inx)  #### ZMIENIŁEM POP(0) NA POP(INX)
        if best_first:
            if parent1.fitness > parent2:
                parent1, parent2 = parent2, parent1  # zamiana kolejności jak rodzic 2 był lepszy

        prev_compound = None
        division_idx = int(parent1.size * random.random())
        for idx, gene in enumerate(parent1):
            if gene.pit == 1 or (prev_compound is not None and prev_compound != gene.compound):  # nastąpi pit stop
                if no_pit == 1:
                    division_idx = idx
                    break
                else:
                    no_pit -= 1
            prev_compound = gene.compound

        child1 = parent1[:division_idx] + parent2[division_idx:]
        child2 = parent2[:division_idx] + parent1[division_idx:]

        population.new_individuals.append(child1)
        population.new_individuals.append(child2)


def pick_parents_tournament(population: NextPopulation, m: int, n: int) -> None:
    """
    Wybranie rodziców turniejowo w m-podzbiorach n-elementowych
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :param m: (int) : liczba podzbiorów parzysta
    :param n: (int) : liczba elementów w podzbiorze
    :return: None
    """
    if m % 2 == 1:
        m += 1
    subsets = []
    for _ in range(m):
        subsets.append(random.sample(population.individuals, n))
    for subset in subsets:
        population.picked_parents.append(max(subset, key = lambda x: x.fitness))


def pick_parents_roulette(population: NextPopulation, m: int, equal_chances: bool = False) -> None:
    """
    Wybranie rodziców ruletką z prawdopodobieństwem równym albo proporcjonalnym
    :param m: (int) : liczba wybranych rodziców
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :param equal_chances: (bool) : czy prawdopodobieństwo wyboru równe
    :return: None
    """
    if equal_chances:
        for _ in range(m):
            random_idx = random.randint(0, len(population.individuals))
            population.picked_parents.append(population.individuals.pop(random_idx))
    else:
        sum_fitness = 0
        for individual in population.individuals:
            sum_fitness += individual.fitness

        for _ in range(m):
            random_value = sum_fitness * random.random()
            fitness_counter = 0
            idx = -1
            while fitness_counter < random_value:
                idx += 1
                fitness_counter = population.individuals[idx].fitness
            picked_individual = population.individuals.pop(idx)
            sum_fitness -= picked_individual.fitness
            population.picked_parents.append(picked_individual)


def adjust_population(population: NextPopulation, best_ancestors: bool = False, elitist: List[Individual] = []) -> None:
    """
    Funkcja uzupełniająca rozmiar populacji
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :param best_ancestors: (bool) : dobieranie od najlpeszych przodków lub losowo
    :param elitist : krótka lista osobników, które jeszcze przed selekcją dostały passa do następnej populacji (domyślnie pusta), funkcja wybierająca te osobniki jest dosłownie pod tą
    :return: None
    """
    #### tutaj w tej funkcji dopisałam tylko ten warunek a tak to zostawiłam bez zmian
    if elitist:
        if len(population.new_individuals) + len(elitist) <= len(population.individuals):
            # jeśli rozmiar nowej populacji połączonej z wybranymi najlepszymi nie przekracza wielkości poprzedniej to można je spokojnie połączyć
            for ind in elitist:
                population.new_individuals.append(ind)
        else:
            while len(population.new_individuals) + len(elitist) > len(population.individuals):
                # jeśli rozmiar populacji okazał się za duży (większy niż poprzednia) to usunięte zostają losowe nowe elementy z nowej populacji, żeby zrobić miejsce dla najlepszych
                # ale możliwe, że taki przypadek tak naprawdę nigdy nie wystąpi?
                random_inx = random.randint(0, len(population.new_individuals)-1)
                population.new_individuals.remove(random_inx)
    ####

    if best_ancestors:
        while len(population.new_individuals) != len(population.individuals):
            ancestors = sorted(population.individuals, key=lambda x: x.fitness, reverse=True)
            population.new_individuals.append(ancestors.pop(0))
    else:
        while len(population.new_individuals) != len(population.individuals):
            random_idx = random.randint(0, len(population.individuals))
            population.new_individuals.append(population.individuals.pop(random_idx))


def cross_agression(population: NextPopulation, random_division_point: bool = False) -> None:
    """
    Krzyżowanie samej agresji z domyślnym punktem podziału w środku osobnika lub w losowo wybranym
    :param random_division_point: (bool) : czy losować punkt podziału do krzyżowania
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :return: None
    """
    while population.picked_parents:
        inx = random.randint(0, len(population.picked_parents) - 1)
        parent1 = population.picked_parents.pop(inx)
        inx = random.randint(0, len(population.picked_parents) - 1)
        parent2 = population.picked_parents.pop(inx)

        if random_division_point:
            midpoint = int(parent1.size * random.random())
        else:
            midpoint = parent1.size // 2

        child1 = parent1[:midpoint] + parent2[midpoint:]
        child2 = parent2[:midpoint] + parent1[midpoint:]

        for i in range(midpoint):
            child1.list_of_laps[i].aggression = parent1.list_of_laps[i].aggression
            child2.list_of_laps[i].aggression = parent2.list_of_laps[i].aggression

        for i in range(midpoint,parent1.size):
            child1.list_of_laps[i].aggression = parent2.list_of_laps[i].aggression
            child2.list_of_laps[i].aggression = parent1.list_of_laps[i].aggression            

        population.new_individuals.append(child1)
        population.new_individuals.append(child2)
##################

def elitist_selection(population: NextPopulation, n: int = 5) -> List[Individual]:
    """
    Wybranie jakiejś małej grupy osobników, która przechodzi od razu do następnej populacji, czyli
    1. wybór tych kilku najlepszych
    2. jeśli faktycznie zostały takie wybrane to przed selekcją rodziców są one usuwane z populacji, żeby potem nie mogły brać udziału w selekcji

    :param population: populacja prztwarzana w i-tej iteracji
    :param n: liczba najlepszych osobników, którą chcemy zachować (domyślnie 5 czyli przy 50 to będzie 1%)
    :return: lista najlepszych osobników
    """

    best_individuals = sorted(population.individuals, key=lambda x: x.fitness, reverse=True)[:n]    # wybór n-najlepszych

    for ind in best_individuals:
        population.individuals.remove(ind)

    if best_individuals:
        return best_individuals
    else:
        return None


def cross_2_points(population: NextPopulation) -> None:
    """
    2 losowe punkty krzyżowania
    :param population:
    :return: None
    """

    while population.picked_parents:
        inx = random.randint(0, len(population.picked_parents) - 1)
        parent1 = population.picked_parents.pop(inx)
        inx = random.randint(0, len(population.picked_parents) - 1)
        parent2 = population.picked_parents.pop(inx)

        point1 = random.radint(0, len(parent1))
        point2 = random.choice([i for i in range(len(parent1)) if i != point1])
        point3 = random.choice([i for i in range(len(parent1)) if i != point1 and i != point2])


        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

        population.new_individuals.append(child1)
        population.new_individuals.append(child2)
