
# laden der benötigten Bibliotheken:
import matplotlib.pyplot as plt
import numpy as np

# Einlesen des Datensatzes. Erste Spalte in time und zweite Spalte in event_value
time, event_value = np.loadtxt("Aufgabe7_CUSUM.txt", unpack = True)

print("Der eingelesene Datensatz enthält " + str(len(time)) + " Werte.")
number = int(input("Anzahl der zu testenen Daten eingeben: "))
if number > len(time):
    print("Number ist größer als der Datensatz (" + str(len(time)) + " Werte)")
    exit()

# Alternativ: number = len(event_value) [für alle Messwerte]

n = float(input("Faktor der Standartabweichung eingeben: "))       # Grenzwertberechnung
w = np.mean(event_value)                                        # Erwartungswert
std_dev = np.std(event_value)
print("Der Mittelwert der Messwerte beträgt: " + str(w))
print("Die Standartabweichung der Messwerte beträgt: " + str(std_dev))
#w = np.average(event_value[0:1000])  # Als Alternative den Erwartungswert eingeben

s = [.0] * number
time_s = time[:number]
i = 0
h = n*std_dev
bool = True
while i < number and bool:
    if i == 0:
        s[i] = (event_value[i] - w)
    else:
        s[i] = s[i-1] + (event_value[i] - w)
    if s[i] < -h or s[i] > h:
        print("CUSUM an der Stelle  " + str(i) + "  zur Zeit  " + str(time[i]) + "  Minuten ab Start der Sonde.")
        bool = False
    i += 1

i -= 1
if bool == True:
    print("Kein CUSUM. s[" + str(i) + "] beträgt: " + str(s[i]))
else:
    print("s[" + str(i) + "] beträgt: " + str(s[i]))

print(s)


# Plotten der Ereignissanzahl (y-Achse) auf die Zeit (x-Achse):
# TODO: Mit Marker und Zeitstempel

plt.plot(time, event_value, "g-",
         time_s, s, "b-")
plt.xlabel('Time')
plt.ylabel('Events')

# Zeigen des Plots
plt.show()
