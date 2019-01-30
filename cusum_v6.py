# Vollversion CUSUM

# benötigte Bibliotheken werden eingebunden

import numpy as np
import time as tm
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Startdatum der Sonde: 20.07.1999
startdate = '20.07.1999'            # TODO: mit Minutenangabe
#Umwandlung in ein passendes Format
startdate_c = datetime.strptime(startdate,'%d.%m.%Y')
#Datensatz einlesen:
time, event_value = np.loadtxt("Aufgabe7_CUSUM.txt", unpack = True)

"""
# Eingabe der Teilanzahl des Datensatzes die mit dem Programm getestet werden sollen
number = int(input("Anzahl der zu testenen Daten eingeben: ")) # = len(event_value)
if number > len(time):
    print("Number ist groesser als der Datensatz (" + str(len(time)) + " Werte)")
    exit()          # Beendet das Programm, falls _number_ zu gross ist
"""

start = tm.time() #Programmlaufzeit überprüfen

#Variable Parameter:
w = np.mean(event_value)	# Mittelwert setzen
h = 100*w                   # Grenzwert
std_abw_max = 150			# maximale Standartabweichung
min_range = 100             # range for the new average value after an event
i = 1;
number = len(time) #Länge des zu überprüfenden Datensatzes


#Textausgabe im Terminal:
print("Der eingelesene Datensatz enthaelt " + str(len(time)) + " Werte.")
print("Die Messung wurde am ",startdate_c+timedelta(minutes=time[0]),"gestartet und am ",startdate_c+timedelta(minutes=time[0]),"beendet" )                                       # Erwartungswert
print("Der Mittelwert der Messwerte betraegt: " + str(w))

#Arrays initialisieren (Laufzeitoptimierung):
s = [0] * number
sp = [0] * number
sn = [0] * number
cusum_points = []
cusum_p_points = []
cusum_n_points = []
converted_time = [0] * number #Array for saving of the converted times


#converting the time array into dates
j = 0
while j < number:
    converted_time[j] = startdate_c + timedelta(minutes=time[j])
    j+=1

#Falls gefordert wird hier die zu überprüfende Sequenz des Datensatzes erstellt
time_s = time[:number]
converted_time_s = converted_time[:number]

# Funktion: setzt neues w (Mittelwert dynamisch); neues i (Index wo das Event zuende ist) wird zurückgegeben
def new_average_and_index(i):
    std_abw = std_abw_max + 1
    while (i+min_range) < number and std_abw > std_abw_max:
        std_abw = np.std(event_value[i:(i+min_range)])
        w = np.mean(event_value[i:(i+min_range)])
        i += 100
    return (i)


#Funktion: setzt neue Startwerte
def new_start(i):
        s[i] = value_current
        sp[i] = value_current
        if sp[i] < 0:
            sp[i] = 0  # sp wird nie < 0
        sn[i] = value_current
        if sn[i] > 0:
            sp[i] = 0  # sn wird nie > 0

# Startinitialisierungen:
i = new_average_and_index(i)
value_current = (event_value[i] - w)
new_start(i)

while i < number: #Hauptschleife

    value_current = (event_value[i] - w)

    s[i] = s[i-1] + value_current
    sp[i] = sp[i-1] + value_current
    if sp[i] < 0:
        sp[i] = 0     # sp wird nie < 0
    sn[i] = sn[i-1] + value_current
    if sn[i] > 0:
        sn[i] = 0     # sn wird nie > 0

    # Hier wird gestet ob der Grenzwert überschritten wird und wenn ja, wird dies als Event ausgegeben und startet CUSUM neu, sobald das Event zuende ist.
    if (s[i] < -h or s[i] > h):
        print("CUSUM an der Stelle  " + str(i) + "  zur Zeit  " + str(startdate_c + timedelta(minutes=time[i])) + ".")
        cusum_points.append(startdate_c + timedelta(minutes=time[i]))
        new_start(i)
        i = new_average_and_index(i)
    if sp[i] > h:
        print("CUSUM+ an der Stelle  " + str(i) + "  zur Zeit  " + str(startdate_c + timedelta(minutes=time[i])) + ".")
        cusum_p_points.append(startdate_c + timedelta(minutes=time[i]))
        new_start(i)
        i = new_average_and_index(i)
    if sn[i] < -h:
        print("CUSUM- an der Stelle  " + str(i) + "  zur Zeit  " + str(startdate_c + timedelta(minutes=time[i])) + ".")
        cusum_n_points.append(startdate_c + timedelta(minutes=time[i]))
        new_start(i)
        i = new_average_and_index(i)

    i += 1



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
        #plt.text(i, 40000, r'C')
        plt.annotate("C",xy=(i,40000),xytext=(i,50000),arrowprops=dict(arrowstyle("->")))#facecolor="black",shrink=0.05),horizontalalignment='center', verticalalignment='top',)
for i in cusum_p_points:
        plt.text(i, 40000, r'C+')
for i in cusum_n_points:
        plt.text(i, 40000, r'C-')
#Formating time axis
#myFmt = mdates.DateFormatter('%m-%d')



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
#myFmt2 = mdates.DateFormatter('%m-%d-%y')
#plt.gca().xaxis.set_major_formatter(myFmt2)

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.3)



ende = tm.time()
print("Laufzeit: " + '{:5.3f}s'.format(ende-start))

# Zeigen des Plots
plt.show()
