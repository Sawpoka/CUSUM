# laden der benötigten Bibliotheken:
import matplotlib.pyplot as plt
import numpy as np


time, event_value = np.loadtxt("Aufgabe7_CUSUM.txt", unpack = True)
number = len(time)
w = np.mean(event_value)
std_abw_max = 100
range = 100             # range for the new average value after an event


def event_over(i):
    wp = 1.2 * w
    wn = 0.8 * w
    while i < number:
        if event_value[i] < wp and event_value[i] > wn:
            return i
        else:
            i += 1

i = 10000

def new_average_and_index(i,range):
    std_abw = std_abw_max + 1
    while (i+range) < number and std_abw > std_abw_max:
        std_abw = np.std(event_value[i:(i+range)])
        w = np.mean(event_value[i:(i+range)])
        i += 100
    return std_abw, (i-99)


std_abw, i = new_average_and_index(i,range)       # w geht offenbar so, i und std_abw muss zurückgegeben und neu überschrieben werden.
print(i)
print(std_abw)
print(w)
