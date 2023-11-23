from data import *
import math

def time_function(osobnik,S,t_pit) :
    f = 0
    for n in range(0,len(osobnik)) :
        f += (Tire.lap_completed()+velocity_e(n)+velocity_m(n))

    f = S/f
    f = f+t_pit
    return f

def velocity_m(n):
    m = n*0.03
    return m

def velocity_e(n):
    e = 1.4-0.3*math.exp^(-0.1*n+1)
    return e