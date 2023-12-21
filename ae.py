from population import *
from operators import *

def evolutionary_algorith(start_size: int, Circuit: Circuit, max_iter: int, number_of_parents: int, num_in_subset:int, selection_type,mutation_probability: int):
    """
    Główny program algorytmu tworzący populacje bazową według 
    : param start_size (int) : wielkość początkowej populacji
    : param Circuit: (Circuit) : tor i jego parametry
    : param max_iter (int) : maksymalna ilość pokoleń
    : param number_of_parents (int)  : liczba rodziców
    : param num_in_subset (int) : liczba
    : param selection_type : typ selekcji (rankingowa czy turniejowa)
    : param mutation_probability (int): prawdopodobieństwo występowania wybraych mutacji
    : param 

    """
    # populacja bazowa
    P_start = NextPopulation([])
    P_start.start_population(start_size,Circuit)
    i = 0
    # każdy osobnik populacji ma od razu przypisaną wartość przystosowania (f. celu)
    P_prev = P_start

    while i < max_iter:     # może być inny warunek stopu np. jeśli któryś osobnik z P_prev ma odpowiednio dobre przystosowanie

        if number_of_parents % 2 != 0:      #  (number_of_parents musi być parzyste bo trzeba ich dobrać w pary)
            number_of_parents += 1

        if selection_type == 'tournament':
            pick_parents_tournament(P_prev,number_of_parents,num_in_subset)
        elif selection_type == 'roulette':
            pick_parents_roulette(P_prev,number_of_parents,num_in_subset)
        else:
            pass


        P_prev.pick_parents(number_of_parents, num_in_subset, 'selekcja')   # to wszystko jest opisane w population
        P_prev.cross()     # krzyżowanie
        P_prev.mutate(mutation_probability)    # mutacja

        # jeszcze pytanie czy nowa populacja jest tworzona tylko z new_individuals czy z new_individual i (old_)individuals
        # i chyba ta druga opcja jest lepsza, bo jeśli byłaby tylko z krzyżowanych rodziców to by się te nowsze populacje cały czas zmniejszały
        P_prev.shuffle_population()

        P_next = NextPopulation(P_prev.new_individuals)

        P_prev = P_next

    # wybierz tego najlepszego osobnika
    return None  # i go zwróć

