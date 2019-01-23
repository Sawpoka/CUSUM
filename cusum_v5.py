#pfeil, datum, mittelwert?, bildschrim einstell, hspace 0,3, zeitabstand nach event


import numpy as np
import time as tm
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Startdatum 20.07.1999
startdate = '20.07.1999'            # TODO: mit Minutenangabe
#Umwandlung in ein passendes Format
startdate_c = datetime.strptime(startdate,'%d.%m.%Y')

time, event_value = np.loadtxt("Aufgabe7_CUSUM.txt", unpack = True)

"""
# Eingabe der Teilanzahl des Datensatzes die mit dem Programm getestet werden sollen
number = int(input("Anzahl der zu testenen Daten eingeben: ")) # = len(event_value)
if number > len(time):
    print("Number ist groesser als der Datensatz (" + str(len(time)) + " Werte)")
    exit()          # Beendet das Programm, falls _number_ zu gross ist
"""

start = tm.time()

number = len(time)
w = np.mean(event_value)
print("Der eingelesene Datensatz enthaelt " + str(len(time)) + " Werte.")
print("Die Messung wurde am ",startdate_c+timedelta(minutes=time[0]),"gestartet und am ",startdate_c+timedelta(minutes=time[0]),"beendet" )                                       # Erwartungswert
print("Der Mittelwert der Messwerte betraegt: " + str(w))


s = [0] * number
sp = [0] * number
sn = [0] * number
cusum_points = []
cusum_p_points = []
cusum_n_points = []
converted_time = [0] * number #Array for saving of the converted times

# Sinnvoll? - oder durchgängig bei Minuten bleiben, aber nur die Ausgaben umrechnen?
#converting the time array into dates
j = 0
while j < len(time):
    converted_time[j] = startdate_c + timedelta(minutes=time[j])
    j+=1

time_s = time[:number]
converted_time_s = converted_time[:number]
h = 150*w                   # Grenzwert
i = 1


# event_over anpassen: neuer gemittelter Mittwert, sobald die Standartabweichung klein genug ist (Immer für 20-200 Werte ? <- variabel!)
# --> neues i (Position) und neues w (Mittelwert)
def event_over(i):
    wp = 1.2 * w
    wn = 0.8 * w
    while i < number:
        if event_value[i] < wp and event_value[i] > wn:
            return i
        else:
            i += 1

def new_start():
        s[i] = value_actual
        sp[i] = value_actual
        if sp[i] < 0:
            sp[i] = 0  # sp wird nie < 0
        sn[i] = value_actual
        if sn[i] > 0:
            sp[i] = 0  # sn wird nie > 0

# set 0
s[0] = event_value[0] - w
sp[0] = event_value[0] - w
if sp[0] < 0:
 sp[0] = 0  # sp wird nie < 0
sn[0] = event_value[0] - w
if sn[0] > 0:
 sp[0] = 0  # sn wird nie > 0

while i < number:

    value_actual = (event_value[i] - w)

    s[i] = s[i-1] + value_actual
    sp[i] = sp[i-1] + value_actual
    if sp[i] < 0:
        sp[i] = 0     # sp wird nie < 0
    sn[i] = sn[i-1] + value_actual
    if sn[i] > 0:
        sn[i] = 0     # sn wird nie > 0

    # Testet ob der Grenzwert überschritten wird und wenn ja, gibt dieses als Event aus und startet CUSUM neu, sobald das Event zuende ist
    if (s[i] < -h or s[i] > h):
        print("CUSUM an der Stelle  " + str(i) + "  zur Zeit  " + str(startdate_c + timedelta(minutes=time[i])) + ".")
        cusum_points.append(startdate_c + timedelta(minutes=time[i]))
        new_start()
        i = event_over(i)
    if sp[i] > h:
        print("CUSUM+ an der Stelle  " + str(i) + "  zur Zeit  " + str(startdate_c + timedelta(minutes=time[i])) + ".")
        cusum_p_points.append(startdate_c + timedelta(minutes=time[i]))
        new_start()
        i = event_over(i)
    if sn[i] < -h:
        print("CUSUM- an der Stelle  " + str(i) + "  zur Zeit  " + str(startdate_c + timedelta(minutes=time[i])) + ".")
        cusum_n_points.append(startdate_c + timedelta(minutes=time[i]))
        new_start()
        i = event_over(i)   # i = event_over_n(i)

    i += 1


# print(detected_points)

# Plotten der Ereignissanzahl (y-Achse) auf die Zeit (x-Achse):
# TODO: Mit Marker und Zeitstempel
#3 DP arrays are for testing
plt.figure(1)
plt.subplot(211)
plt.plot(converted_time_s, event_value, "g-")
plt.title('Event overview')
# plt.xlabel('Time')
plt.ylabel('#')
for i in cusum_points:
        plt.text(i, 40000, r'C')
        # plt.annotate("C",xy=(i[0],i[1]*1.3),xytext=(i[0],i[1]*1.7),arrowprops=dict(facecolor="black",shrink=0.05),)       # Hinzufügen des richtigen cusum_points -Array nötig
for i in cusum_p_points:
        plt.text(i, 40000, r'C+')
for i in cusum_n_points:
        plt.text(i, 40000, r'C-')
#Formating time axis
plt.gcf().autofmt_xdate()
myFmt = mdates.DateFormatter('%m-%d')
plt.gca().xaxis.set_major_formatter(myFmt)



plt.subplot(212)
plt.plot(converted_time_s, s, "b-",label='S')
plt.plot(converted_time_s, sp, "y-",label='SP')
plt.plot(converted_time_s, sn, "r-",label='SN')
plt.title('Cusum overview')
plt.xlabel('Time after Start')
plt.ylabel('#')
legend = plt.legend(loc='upper left', shadow=True, fontsize='x-small')
#legend.get_frame().set_facecolor("C0") Farbe der Legende
#Formating time axis
plt.gcf().autofmt_xdate()
myFmt2 = mdates.DateFormatter('%m-%d')
plt.gca().xaxis.set_major_formatter(myFmt2)         ### WARUM GEHT DIE BESSERE DATUMSANZEIGE NICHT BEI BEIDEN?

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.3)



ende = tm.time()
print("Laufzeit: " + '{:5.3f}s'.format(ende-start))

# Zeigen des Plots
plt.show()
