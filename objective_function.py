from data import *
import math

def time_function(list_of_laps: List[List[int]],circuit: Circuit): # zmienione arg z O na N, list_of_laps, bo O powstaje dopiero po wyliczeniu tej funkcji
    """
    :param list_oflaps (List[List[int]]) : Gen, lista krotek dla każdego okrążenia
    :param circuit (Circuit) : Dane wyscigu
    """
    k_pit = 0 #licznik pitstopów
    f = 0 #
    for n in range(circuit.no_laps) : #osobnik: N*[p,A,o]
        tires = Circuit.get_tires() #pobranie posortowanej liczby opon 

        if (n>0 and list_of_laps[n][2]!=list_of_laps[n-1][2]) or list_of_laps[n][0]==1: #czy nastąpił pitstop lub zmiana opony 
            k_pit += 1
            if list_of_laps[n][2]== circuit.Compound.SOFT.value: #zmiana na mieszankę miękką
                if tires[circuit.Compound.SOFT.value]==0: #czy zostały jeszcze miękkie opony
                    return math.inf

                new_tire = tires[circuit.Compound.SOFT.value].pop(0)

            elif list_of_laps[n][2]== circuit.Compound.MEDIUM.value: #zmiana na mieszankę pośrednią
                if tires[circuit.Compound.SOFT.value]==0: #czy zostały jeszcze miękkie opony
                    return math.inf
                
                new_tire = tires[circuit.Compound.MEDIUM.value].pop(0)

            else: #zmiana na mieszankę twardą
                if tires[circuit.Compound.SOFT.value]==0: #czy zostały jeszcze miękkie opony
                    return math.inf
                
                new_tire = tires[circuit.Compound.HARD.value].pop(0)

            if new_tire.lap_completed(list_of_laps[n][1])==0 : #czy opona pękła
                if tires[circuit.Compound.SOFT.value]==0: #czy zostały jeszcze miękkie opony
                    return math.inf
            
                return math.inf
            
            f += (new_tire.lap_completed(list_of_laps[n][1])+velocity_e(n)+velocity_m(n)) #dodanie prędkości na n-tym okrążeniu dla nowej opony

        else : 
            f += (new_tire.lap_completed(list_of_laps[n][1])+velocity_e(n)+velocity_m(n)) #dodanie prędkości na n-tym okrążeniu

    if k_pit==0: #czy wystąpił przynajmniej jeden pitstop
        return math.inf

    f = f/circuit.no_laps #średnia prędkości na jedno okrążenie
    f = circuit.track_dist/f 
    f = f+circuit.t_pit*k_pit #dodanie czasów pitstopów
    return f

def velocity_m(n):
    m = n*0.03
    return m

def velocity_e(n):
    e = 1.4-0.3*math.exp^(-0.1*n+1)
    return e