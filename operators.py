import random
from population import *
from typing import Union


def mutate_aggression(population: Union[NextPopulation, StartPopulation], probability: float = 0.03) -> None:
    """
    Mutacja tylko agresji z zadanym prawdpopodbieństwem (domyślnie 0.05)
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
                aggressions = list(Aggression)
                aggressions.remove(gene.aggression)
                new_aggression = random.choices(aggressions, [0.25, 0.25, 0.25, 0.25])[0]
                gene.aggression = new_aggression


def mutate_pit(population: Union[NextPopulation, StartPopulation], probability: float = 0.05) -> None:
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


def mutate_compound(population: Union[NextPopulation, StartPopulation], probability: float = 0.05) -> None:
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


def cross(population: Union[NextPopulation, StartPopulation], random_division_point: bool = False) -> None:
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


def cross_before_pit(population: Union[NextPopulation, StartPopulation], no_pit: int = 1, best_first: bool = False) -> None:
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


def pick_parents_tournament(population: Union[NextPopulation, StartPopulation], m: int, n: int) -> None:
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
        population.picked_parents.append(max(subset, lambda x: x.fitness))


def pick_parents_roulette(population: Union[NextPopulation, StartPopulation], m: int, equal_chances: bool = False) -> None:
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


def adjust_population(population: Union[NextPopulation, StartPopulation], best_ancestors: bool = False) -> None:
    """
    Funkcja uzupełniająca rozmiar populacji
    :param population: (Union[NextPopulation, StartPopulation]) : populacja
    :param best_ancestors: (bool) : dobieranie od najlpeszych przodków lub losowo
    :return: None
    """
    if best_ancestors:
        while len(population.new_individuals) != len(population.individuals):
            ancestors = sorted(population.individuals, key=lambda x: x.fitness, reverse=True)
            population.new_individuals.append(ancestors.pop(0))
    else:
        while len(population.new_individuals) != len(population.individuals):
            random_idx = random.randint(0, len(population.individuals))
            population.new_individuals.append(population.individuals.pop(random_idx))
