from data import *
from population import *


def evolutionary_algorith(start_size, Circuit, max_iter, number_of_parents, num_in_subset):

    # populacja bazowa
    P_start = StartPopulation(start_size, Circuit)
    i = 0
    # każdy osobnik populacji ma od razu przypisaną wartość przystosowania (f. celu)
    P_prev = P_start

    while i < max_iter:     # może być inny warunek stopu np. jeśli któryś osobnik z P_prev ma odpowiednio dobre przystosowanie

        if number_of_parents % 2 != 0:      #  (number_of_parents musi być parzyste bo trzeba ich dobrać w pary)
            number_of_parents += 1

        P_prev.pick_parents(number_of_parents, num_in_subset)   # to wszystko jest opisane w population
        P_prev.cross()     # krzyżowanie
        P_prev.mutate()    # mutacja

        # jeszcze pytanie czy nowa populacja jest tworzona tylko z new_individuals czy z new_individual i (old_)individuals
        # i chyba ta druga opcja jest lepsza, bo jeśli byłaby tylko z krzyżowanych rodziców to by się te nowsze populacje cały czas zmniejszały
        P_prev.shuffle_population()

        P_next = NextPopulation(P_prev.new_individuals)

        P_prev = P_next

    # wybierz tego najlepszego osobnika
    return None  # i go zwróć

