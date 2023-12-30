from population import *
from operators import *
import time


def evolutionary_algorithm(start_size: int, circuit: Circuit, max_iter: int, parents_percentage: int,
                           selection_type: int, cross_type: int, cross_prob: int, mutation_aggr: int,
                           mutation_prob1: int, mutation_comp: int, mutation_prob2: int, mutation_pit: int,
                           mutation_prob3: int):
    """
    Główny program algorytmu tworzący populacje bazową według 
    : param start_size (int) : wielkość początkowej populacji
    : param Circuit: (Circuit) : tor i jego parametry
    : param max_iter (int) : maksymalna ilość pokoleń
    : param parents_percentage (int) : ile procent rodziców poddawanych jest reprodukcji
    : param selection_type (int) : typ selekcji (rankingowa czy turniejowa)
    : param cross_type (int) : które krzyżowanie jest włączone
    : param cross_prob (int) : prawdopodobieństwo krzyżowania w kolejych iteracjach
    : param mutation_aggr (int)) : czy mutacja agresji jest włączona
    : param mutation_prob1 (int): prawdopodobieństwo występowania mutacji 1
    : param mutation_comp (int) : czy mutacja mieszanki jest włączona
    : param mutation_prob2 (int): prawdopodobieństwo występowania mutacji 2
    : param mutation_pit (int) : czy mutacja pitstopu jest włączona
    : param mutation_prob3 (int): prawdopodobieństwo występowania mutacji 3
    : return : Lista czasu,liczby iteracji, najlepszego osobnika, iteracji w której został znaleziony, lista najlepszych osobników w kolejnych iteracjach
    """
    start_time = time.time() #czas początkowy

    #zmiana procentów na ułamki:
    parents_percentage = parents_percentage/100
    cross_prob = cross_prob/100
    mutation_prob1 = mutation_prob1/100
    mutation_prob2 = mutation_prob1/100
    mutation_prob3 = mutation_prob1/100

    # populacja bazowa
    P_start = NextPopulation([], circuit)
    P_start.start_population(start_size)
    i = 0
    best_individuals = [] #list najlepszych osobników w każdej iteracji potrzebna do wykresu
    best_individual = copy.copy(min(P_start.individuals, key=lambda x: x.fitness)) #najlepszy osobnik startowej populacji
    best_individuals.append(best_individual)
    print(best_individual)
    best_i = i #pierwsze pokolenie najlepszego osobnika
    # każdy osobnik populacji ma od razu przypisaną wartość przystosowania (f. celu)
    P_prev = P_start

    while i < max_iter:     # może być inny warunek stopu np. jeśli któryś osobnik z P_prev ma odpowiednio dobre przystosowanie
        
        i += 1  # kolejne pokolenie

        #selekcja
        if selection_type == 1:
            pick_parents_tournament(P_prev, int(parents_percentage*P_prev.size), int(0.2*P_prev.size))
        elif selection_type == 0:
            pick_parents_roulette(P_prev, int(parents_percentage*P_prev.size))
        else:
            pass

        #krzyżowanie
        #warunki uruchomienia poszczególnych krzyżowań wybranych orzez użytkownika
        if cross_prob > random.random():
            if cross_type == 0:
                cross(P_prev)
            if cross_type == 1:
                cross(P_prev, True)
            elif cross_type == 2:
                cross_before_pit(P_prev, 2)
            elif cross_type == 3:
                cross_agression(P_prev, True)
            elif cross_type == 4:
                cross_2_points(P_prev)
            else: 
                P_prev.new_individuals = P_prev.individuals
        else:
            P_prev.new_individuals = P_prev.individuals

        #Łączenie pewniej części rodziców i stworzonych potomków ,aby stworzyć nowe pokolenie
        P_prev.shuffle_population()

        # mutacja
        # warunki uruchomienia poszczególnych mutacji wybranych orzez użytkownika z odpowiednim prawdopodobieństwem
        if mutation_aggr == 1:
            mutate_aggression(P_prev, mutation_prob1)
        if mutation_comp == 1:
            mutate_compound(P_prev, mutation_prob2)
        if mutation_pit == 1:
            mutate_pit(P_prev, mutation_prob3)
        
        temp_best_individual = copy.copy(min(P_prev.new_individuals, key=lambda x: x.fitness))
        best_individuals.append(temp_best_individual)
        # sprawdzanie czy został znaleziony lepszy osobnik
        if best_individual.fitness>temp_best_individual.fitness:
            best_individual = temp_best_individual
            best_i = i #aktualizacja pokolenia najlepszego osobnika

        if best_individual.fitness < 70: #warunek satysfakconującego rozwiązania (Nie wiem jaka wartość)
            break

        #następna populacja stworzona z x% najlepszych rodziców i stworzyonych potomków
        P_next = NextPopulation(P_prev.new_individuals,circuit)

        P_prev = P_next

    total_time = time.time() - start_time

    return total_time, i, best_individual, best_i, best_individuals  # Zwrócenie czasu trwania algorytmu,liczby iteracji,najlepszego osobonika, oraz w której iteracji został znaleziony, lista najlepszych osobników w kolejnych iteracjach

