
import numpy as np
import matplotlib.pyplot as plt
import time as tm



time, event_value = np.loadtxt("Aufgabe7_CUSUM.txt", unpack = True)

# print("Der eingelesene Datensatz enthält " + str(len(time)) + " Werte.")
#
# Eingabe der Teilanzahl des Datensatzes die mit dem Programm getestet werden sollen
# number = int(input("Anzahl der zu testenen Daten eingeben: ")) # = len(event_value)
# if number > len(time):
#    print("Number ist größer als der Datensatz (" + str(len(time)) + " Werte)")
#    exit()          # Beendet das Programm, falls _number_ zu groß ist
#

start = tm.time()

number = (len(time))

w = np.mean(event_value)                                        # Erwartungswert
print("Der Mittelwert der Messwerte beträgt: " + str(w))


s = [.0] * number
sp = [.0] * number
sn = [.0] * number
detected_points = [0] * number
time_s = time[:number]
h = 5*w                   # Grenzwert
i = 0
bool = True
boolp = True
booln = True
while i < number:
    #ALT: value_negative = min(0, event_value[i] - w)
    #ALT: value_positive = max(0, event_value[i] - w)
    value_actual = (event_value[i] - w)     #ALT: min(0, event_value[i] - w) + max(0, event_value[i] - w)
    if i == 0:
        s[i] = value_actual
        sp[i] = value_actual
        if sp[i] < 0: sp[i] = 0  # sp wird nie < 0
        sn[i] = value_actual
        if sn[i] > 0: sp[i] = 0  # sn wird nie > 0
    else:
        s[i] = s[i-1] + value_actual    #ALT: + (event_value[i] - w)
        sp[i] = sp[i-1] + value_actual
        if sp[i] < 0: sp[i] = 0     # sp wird nie < 0
        sn[i] = sn[i-1] + value_actual
        if sn[i] > 0: sn[i] = 0     # sn wird nie > 0

    if (s[i] < -h or s[i] > h) and bool:
        print("CUSUM an der Stelle  " + str(i) + "  zur Zeit  " + str(time[i]) + "  Minuten ab Start der Sonde.")
        bool = False
    if sp[i] > h and boolp:
        print("CUSUM+ an der Stelle  " + str(i) + "  zur Zeit  " + str(time[i]) + "  Minuten ab Start der Sonde.")
        boolp = False
    if sn[i] < -h and booln:
        print("CUSUM- an der Stelle  " + str(i) + "  zur Zeit  " + str(time[i]) + "  Minuten ab Start der Sonde.")
        booln = False
    i += 1

i -= 1
if bool == True:
    print("Kein CUSUM. s[" + str(i) + "] beträgt: " + str(s[i]))
else:
    print("s[" + str(i) + "] beträgt: " + str(s[i]))
if boolp == True:
    print("Kein CUSUM+. sp[" + str(i) + "] beträgt: " + str(s[i]))
else:
    print("sp[" + str(i) + "] beträgt: " + str(s[i]))
if booln == True:
    print("Kein CUSUM-. sn[" + str(i) + "] beträgt: " + str(s[i]))
else:
    print("sn[" + str(i) + "] beträgt: " + str(s[i]))

# Plotten der Ereignissanzahl (y-Achse) auf die Zeit (x-Achse):
# TODO: Mit Marker und Zeitstempel
detected_points[10000]=7718419
detected_points[20000]=7730000
detected_points[30000]=7740000
plt.figure(1)
plt.subplot(211)
plt.plot(time, event_value, "g-")
plt.title('Event overview')
plt.xlabel('Time after Start')
plt.ylabel('#')
for i in detected_points:
	if i != 0:
		plt.text(i, 40000, r'ED')

plt.subplot(212)
plt.plot(time_s, s, "b-",label='S')
plt.plot(time_s, sp, "y-",label='SP')
plt.plot(time_s, sn, "r-",label='SN')
plt.title('Cusum overview')
plt.xlabel('Time after Start')
plt.ylabel('#')
legend = plt.legend(loc='upper left', shadow=True, fontsize='x-small')
#legend.get_frame().set_facecolor("C0") Frabe der Legende


ende = tm.time()
print("Laufzeit: " + '{:5.3f}s'.format(ende-start))

# Zeigen des Plots
plt.show()
