# laden der benötigten Bibliotheken:
import matplotlib.pyplot as plt
import numpy as np

# Einlesen des Datensatzes. Erste Spalte in time und zweite Spalte in event_value
time, event_value = np.loadtxt("Aufgabe7_CUSUM.txt", unpack = True)

# Einlesen/Ausrechnen eines Mittelwertes:
# w = float(input("Mittelwert eingeben: "))
w = np.average(event_value)
std_dev = np.std(event_value)
print(std_dev)
print(w)

# Durchführen des Cusums verfahrens: Berechnung der Abweichungen und ausgeben des Summer dieser

c = 0.0
i = 0
while i < len(event_value):
    c = c + (event_value[i] - w)
    i += 1


print(c)



# Plotten der Ereignissanzahl (y-Achse) auf die Zeit (x-Achse):
# TODO: Mit Marker und Zeitstempel

plt.plot(time, event_value, "g-")
plt.xlabel('Time')
plt.ylabel('Events')

# Zeigen des Plots
plt.show()
