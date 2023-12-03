from data import *
from population import *


def evolutionary_algorith(start_size, Circuit, max_iter):

    # populacja bazowa
    P_start = StartPopulation(start_size, Circuit)
    i = 0
    # każdy osobnik populacji ma od razu przypisaną wartość przystosowania (f. celu)
    P_prev = P_start

    while i < max_iter:     # może być inny warunek stopu np. jeśli któryś osobnik z P_prev ma odpowiednio dobre przystosowanie

        P_prev.pick_parents()  # selekcja
        P_prev.cross()     # krzyżowanie
        P_prev.mutate()    # mutacja

        P_next = NextPopulation(P_prev)

        P_prev = P_next

    # wybierz tego najlepszego osobnika
    return None  # i go zwróć

