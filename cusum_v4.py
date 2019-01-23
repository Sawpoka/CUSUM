# CUSUM New - Formel nach Wikipedia - Orientierung an cusum_felix und test_cusum
#pfeil, mittelwert?,zeitabstand nach event


import numpy as np
import time as tm
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Startdatum 20.07.1999
startdate = '20.07.1999'
#Umwandlung in ein passendes Format
startdate_c = datetime.strptime(startdate,'%d.%m.%Y')

time, event_value = np.loadtxt("Aufgabe7_CUSUM.txt", unpack = True)

"""print("Der eingelesene Datensatz enthaelt " + str(len(time)) + " Werte.")

# Eingabe der Teilanzahl des Datensatzes die mit dem Programm getestet werden sollen
number = int(input("Anzahl der zu testenen Daten eingeben: ")) # = len(event_value)
if number > len(time):
    print("Number ist groesser als der Datensatz (" + str(len(time)) + " Werte)")
    exit()          # Beendet das Programm, falls _number_ zu gross ist
"""
start = tm.time()
number = len(time)
w = np.mean(event_value)
print("Die Messung wurde am ",startdate_c+timedelta(minutes=time[0]),"gestartet und am ",startdate_c+timedelta(minutes=time[number-1]),"beendet" )                                       # Erwartungswert
print("Der Mittelwert der Messwerte betraegt: " + str(w))


s = [0] * number
sp = [0] * number
sn = [0] * number
detected_points = []
converted_time = [0] * number #Array for saving of the converted times
time_s = time[:number]
h = 100*w                   # Grenzwert
i = 1


#CUSUM initialisieren
s[0] = event_value[0] - w
sp[0] = event_value[0] - w
if sp[0] < 0:
 sp[0] = 0  # sp wird nie < 0
sn[0] = event_value[0] - w
if sn[0] > 0:
 sp[0] = 0  # sn wird nie > 0

j = 0
while j < len(time):#converting the time array into dates
 converted_time[j] = startdate_c + timedelta(minutes=time[j])
 j+=1

while i < number:
    #ALT: value_negative = min(0, event_value[i] - w)
    #ALT: value_positive = max(0, event_value[i] - w)
 value_actual = (event_value[i]-w)     #ALT: min(0, event_value[i] - w) + max(0, event_value[i] - w)
 s[i] = s[i-1] + value_actual
 sp[i] = sp[i-1] + value_actual
 if sp[i] < 0:
  sp[i] = 0     # sp wird nie < 0
 sn[i] = sn[i-1] + value_actual
 if sn[i] > 0:
  sn[i] = 0     # sn wird nie > 0

#Test ob Grentzwert
 if (s[i] < -h or s[i] > h):
  print("CUSUM an der Stelle  " + str(i) + "  ,  " + str(time[i]-time[0]) + "  Minuten nach Start der Messung.")
  s[i] = value_actual
  sp[i] = value_actual
  detected_points.append([startdate_c + timedelta(minutes=time[i]),event_value[i]])
  if sp[i] < 0:
   sp[i] = 0  # sp wird nie < 0
  sn[i] = value_actual
  if sn[i] > 0:
   sp[i] = 0  # sn wird nie > 0
  i = i + 1000
 if sp[i] > h:
  print("CUSUM an der Stelle  " + str(i) + "  ,  " + str(time[i]-time[0]) + "  Minuten nach Start der Messung.")
  s[i] = value_actual
  sp[i] = value_actual
  if sp[i] < 0:
   sp[i] = 0  # sp wird nie < 0
  sn[i] = value_actual
  if sn[i] > 0:
   sp[i] = 0  # sn wird nie > 0
  detected_points.append([startdate_c + timedelta(minutes=time[i]),event_value[i]])
  i += 1000
 if sn[i] < -h:
  print("CUSUM an der Stelle  " + str(i) + "  ,  " + str(time[i]-time[0]) + "  Minuten nach Start der Messung.")
  s[i] = value_actual
  sp[i] = value_actual
  if sp[i] < 0:
   sp[i] = 0  # sp wird nie < 0
  sn[i] = value_actual
  if sn[i] > 0:
   sp[i] = 0  # sn wird nie > 0
  detected_points.append([startdate_c + timedelta(minutes=time[i]),event_value[i]])
  i += 1000
 i += 1



# Plotten der Ereignissanzahl (y-Achse) auf die Zeit (x-Achse):
# TODO: Mit Marker und Zeitstempel
#3 DP arrays are for testing
plt.figure(1)
plt.subplot(211)
plt.plot(converted_time, event_value, "g-")
plt.title('Event overview')
plt.xlabel('Time after Start')
plt.ylabel('#')
for i in detected_points:
 #plt.text(i, 40000, r'ED')
 plt.annotate("ED",xy=(i[0],i[1]*1.3),xytext=(i[0],i[1]*1.7),arrowprops=dict(facecolor="black",shrink=0.05),
 )
#Formating time axis
plt.gcf().autofmt_xdate()
myFmt = mdates.DateFormatter('%m-%d')
plt.gca().xaxis.set_major_formatter(myFmt)



plt.subplot(212)
plt.plot(converted_time, s, "b-",label='S')
plt.plot(converted_time, sp, "y-",label='SP')
plt.plot(converted_time, sn, "r-",label='SN')
plt.title('Cusum overview')
plt.xlabel('Time after Start')
plt.ylabel('#')
legend = plt.legend(loc='upper left', shadow=True, fontsize='x-small')
#legend.get_frame().set_facecolor("C0") Frabe der Legende
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.3)


ende = tm.time()
print("Laufzeit: " + '{:5.3f}s'.format(ende-start))

# Zeigen des Plots
plt.show()
