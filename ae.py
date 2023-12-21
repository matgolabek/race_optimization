from population import *
from operators import *
import time

def evolutionary_algorith(start_size: int, Circuit: Circuit, max_iter: int, parents_percentage: int, selection_type,mutation_probability: int):
    """
    Główny program algorytmu tworzący populacje bazową według 
    : param start_size (int) : wielkość początkowej populacji
    : param Circuit: (Circuit) : tor i jego parametry
    : param max_iter (int) : maksymalna ilość pokoleń
    : param parents_percentage (int) : ile procent rodziców poddawanych jest reprodukcji
    : param selection_type : typ selekcji (rankingowa czy turniejowa)
    : param mutation_probability (int): prawdopodobieństwo występowania wybraych mutacji
    : param 

    """
    start_time = time.time() #czas początkowy

    # populacja bazowa
    P_start = NextPopulation([])
    P_start.start_population(start_size,Circuit)
    i = 0
    best_individual = max(P_start.individuals, key = lambda x: x.fitness) #najlepszy osobnik startowej populacji
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
        #warunki uruchomienia poszczególnych krzyżowań wybranych orzez urzytkownika

        #mutacja
        #warunki uruchomienia poszczególnych mutacji wybranych orzez urzytkownika z odpowiednim prawdopodobieństwem

        #P_prev.shuffle_population()

        #następna populacja stworzona z x% najlepszych rodziców i stworzyonych potomków
        #P_next = NextPopulation(P_prev.new_individuals)

        #P_prev = P_next

        # sprawdzanie czy został znaleziony lepszy osobnik
        if (best_individual.fitness<max(P_prev.individuals, key = lambda x: x.fitness).fitness):
            best_individual = max(P_prev.individuals, key = lambda x: x.fitness)
            best_i = i #aktualizacja pokolenia najlepszego osobnika

        if (best_individual.fitness < 60): #warunek satysfakconującego rozwiązania (Nie wiem jaka wartość)
            break

        total_time = time.time() - start_time

    return [total_time,i,best_individual,best_i]  # Zwrócenie czasu trwania algorytmu,liczby iteracji,najlepszego osobonika, oraz w której iteracji został znaleziony

