import math
from data import *

def time_function(list_of_laps ,circuit):
    """
    Funkcja celu obliczająca sumaryczny czas przejazdu 
    :param list_oflaps (List[PartialIndividual]) : Gen, lista krotek dla każdego okrążenia
    :param circuit (Circuit) : Dane wyscigu
    """
    k_pit = 0 #licznik pitstopów
    f = 0 #czas
    for n in range(circuit.no_laps) : #osobnik: N*[p,A,o]
        tires = circuit.get_tires() #pobranie posortowanej liczby opon

        if (n>0 and list_of_laps[n].compound!=list_of_laps[n-1].compound) or list_of_laps[n].pit==1 or n==0: #czy nastąpił pitstop lub zmiana opony 
            k_pit += 1
            if list_of_laps[n].compound== Compound.SOFT.value: #zmiana na mieszankę miękką
                if len(tires[Compound.SOFT.value])==0: #czy zostały jeszcze miękkie opony
                    return math.inf

                new_tire = tires[Compound.SOFT.value].pop(0) #pobranie nowej opony

            elif list_of_laps[n].compound== Compound.MEDIUM.value: #zmiana na mieszankę pośrednią
                if len(tires[Compound.MEDIUM.value])==0: #czy zostały jeszcze miękkie opony
                    return math.inf
                
                new_tire = tires[Compound.MEDIUM.value].pop(0)

            else: #zmiana na mieszankę twardą
                if len(tires[Compound.HARD.value])==0: #czy zostały jeszcze miękkie opony
                    return math.inf
                
                new_tire = tires[Compound.HARD.value].pop(0)

            if new_tire.lap_completed(list_of_laps[n].aggression)==0 : #czy opona pękła 
                return math.inf
            
            f += (new_tire.lap_completed(list_of_laps[n].aggression)+velocity_e(n)+velocity_m(n)) #dodanie prędkości na n-tym okrążeniu dla nowej opony

        else : 
            f += (new_tire.lap_completed(list_of_laps[n].aggression)+velocity_e(n)+velocity_m(n)) #dodanie prędkości na n-tym okrążeniu

    if k_pit==0: #czy wystąpił przynajmniej jeden pitstop
        return math.inf

    f = f/circuit.no_laps #średnia prędkości na jedno okrążenie
    f = circuit.track_dist/f # długosc jednego okrążenia podzielona przez średnią prędkość na jedno okrążenie
    f = f+circuit.t_pit*k_pit #dodanie czasów pitstopów
    return f

def velocity_m(n):
    """
    Funkcja zwraca prędkość w zależności od masy bolidu na danym okrążeniu
    :param n(int) : aktualne okrążenie
    """
    m = n*0.03
    return m

def velocity_e(n):
    """
    Funkcja zwraca prędkość w zależności od ewulucji toru na danym okrążeniu
    :param n(int) : aktualne okrążenie 
    """
    e = 1.4-0.3*float(math.exp(-0.1*n+1))
    return e