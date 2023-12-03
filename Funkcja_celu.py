from data import *
import math

def time_function(O,C) :
    f = 0
    for n in range(O.N) : #osobnik: N*[p,A,o]
        if (n>0 and O.list_of_laps[n][2]!=O.list_of_laps[n-1][2]) or O.list_of_laps[n][0]==1:
            if O.list_of_laps[n][2]== 1:
                pass
            elif O.list_of_laps[n][2]== 2:
                pass
            else:
                pass

            f += (new_tire.lap_completed(O.list_of_laps[n][1])+velocity_e(n)+velocity_m(n))
        else :
            f += (new_tire.lap_completed(O.list_of_laps[n][1])+velocity_e(n)+velocity_m(n))

    f = f/O.N
    f = C.track_dist/f
    f = f+C.t_pit
    return f

def velocity_m(n):
    m = n*0.03
    return m

def velocity_e(n):
    e = 1.4-0.3*math.exp^(-0.1*n+1)
    return e