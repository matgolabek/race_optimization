from population import *
from operators import *
import time

def evolutionary_algorith(start_size: int, circuit: Circuit, max_iter: int, parents_percentage: int, selection_type: str,cross_type : int,mutation_aggr: bool,mutation_prob1: float,mutation_comp: bool,mutation_prob2: float,mutation_pit: bool,mutation_prob3: float):
    """
    Główny program algorytmu tworzący populacje bazową według 
    : param start_size (int) : wielkość początkowej populacji
    : param Circuit: (Circuit) : tor i jego parametry
    : param max_iter (int) : maksymalna ilość pokoleń
    : param parents_percentage (int) : ile procent rodziców poddawanych jest reprodukcji
    : param selection_type (str) : typ selekcji (rankingowa czy turniejowa)
    : param cross_type (int) : które krzyżowanie jest włączone
    : param mutation_aggr (int)) : czy mutacja agresji jest włączona
    : param mutation_prob1 (float): prawdopodobieństwo występowania mutacji 1
    : param mutation_comp (int) : czy mutacja mieszanki jest włączona
    : param mutation_prob2 (float): prawdopodobieństwo występowania mutacji 2
    : param mutation_pit (int) : czy mutacja pitstopu jest włączona
    : param mutation_prob3 (float): prawdopodobieństwo występowania mutacji 3
    : return : Lista czasu,liczby iteracji, najlepszego osobnika, iteracji w której został znaleziony
    """
    start_time = time.time() #czas początkowy

    # populacja bazowa
    P_start = NextPopulation([],circuit)
    P_start.start_population(start_size)
    i = 0
    best_individual = min(P_start.individuals, key = lambda x: x.fitness) #najlepszy osobnik startowej populacji
    print(best_individual)
    best_i = i #pierwsze pokolenie najlepszego osobnika
    # każdy osobnik populacji ma od razu przypisaną wartość przystosowania (f. celu)
    P_prev = P_start

    while i < max_iter:     # może być inny warunek stopu np. jeśli któryś osobnik z P_prev ma odpowiednio dobre przystosowanie
        
        i+=1 # kolejne pokolenie

        #selekcja
        if selection_type == 'tournament':
            pick_parents_tournament(P_prev,int(parents_percentage*P_prev.size),int(0.2*P_prev.size))
        elif selection_type == 'roulette':
            pick_parents_roulette(P_prev,int(parents_percentage*P_prev.size))
        else:
            pass

        #krzyżowanie
        #warunki uruchomienia poszczególnych krzyżowań wybranych orzez użytkownika
        if cross_type == 0:
            cross(P_prev,True)
        elif cross_type == 1:
            cross_agression(P_prev,True)
        else:
            pass
        
        #mutacja
        #warunki uruchomienia poszczególnych mutacji wybranych orzez użytkownika z odpowiednim prawdopodobieństwem
            if mutation_aggr == 1:
                mutate_aggression(P_prev,mutation_prob1)
            if mutation_comp == 1:
                mutate_compound(P_prev,mutation_prob2)
            if mutation_pit == 1:
                mutate_pit(P_prev,mutation_prob3)

        #Łączenie pewniej części rodziców i stworzonych potomków ,aby stworzyć nowe pokolenie
        P_prev.shuffle_population()

        #następna populacja stworzona z x% najlepszych rodziców i stworzyonych potomków
        P_next = NextPopulation(P_prev.new_individuals,circuit)

        P_prev = P_next

        # sprawdzanie czy został znaleziony lepszy osobnik
        if (best_individual.fitness>min(P_prev.individuals, key = lambda x: x.fitness).fitness):
            best_individual = min(P_prev.individuals, key = lambda x: x.fitness)
            best_i = i #aktualizacja pokolenia najlepszego osobnika

        if (best_individual.fitness < 60): #warunek satysfakconującego rozwiązania (Nie wiem jaka wartość)
            break

        total_time = time.time() - start_time

    return [total_time,i,best_individual,best_i]  # Zwrócenie czasu trwania algorytmu,liczby iteracji,najlepszego osobonika, oraz w której iteracji został znaleziony

