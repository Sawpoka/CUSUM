# Testplot

# laden der benötigten Bibliotheken
import matplotlib.pyplot as plt
import numpy as np

# Einlesen des Datensatzes. Erste Spalte in time und zweite Spalte in event_value
time, event_value = np.loadtxt("Aufgabe7_CUSUM.txt", unpack = True)

#Einlesen eines geschätzten Mittelwertes.
w = float(input("Mittelwert eingeben: "))





# Plotten der Ereignissanzahl (y-Achse) auf die Zeit (x-Achse)
plt.plot(time, event_value, "g-")
plt.xlabel('Time')
plt.ylabel('Events')

# Zeigen des Plots
plt.show()
