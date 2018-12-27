###########################
import numpy as np
import matplotlib.pyplot as plt
import time
start = time.time()

number = 10000

times, values = np.loadtxt("Aufgabe7_CUSUM.txt",  unpack=True)
#dev = np.std(values)
dev = np.mean(values)
print(dev)
#w = input("Chose threhhold value: ")
#w = float(w)

def sp(arr,n,w):
    i = 0
    ret = 0
    while i < n:
        ret = max(0,ret + arr[i] - w)
        i+=1
    if ret > 0:
        return ret
    else:
        return 0


def sm(arr,n,w):
    i = 0
    ret = 0
    while i < n:
        ret = -min(0,-(ret -arr[i] + w))
        i+=1
    if ret > 0:
        return ret
    else:
        return 0

def sn(arr,n,w):
    i = 0
    ret = 0
    while i < n:
        ret = ret + arr[i] - w
        i+=1
    return ret
cnt = 0
spp = []

smm = []
snn = []
points = np.zeros(number)
while cnt < number:
    spp.append(round(sp(values,cnt,dev),2))
    smm.append(round(sm(values,cnt,dev),2))
    v=round(sn(values,cnt,dev),2)
    snn.append(v)

    if v > dev:
        points[cnt] = values[cnt]
    cnt +=1

t = times[0:number]
v = values[0:number]
f,sp = plt.subplots(5,1)
sp1=sp[0]
sp2=sp[1]
sp3=sp[2]
sp4=sp[3]
sp5=sp[4]
sp1.plot(t,spp)
sp2.plot(t,smm)
sp3.plot(t,snn)
sp4.plot(t,points)
sp5.plot(t,v)
plt.xlabel("Time after start")
plt.ylabel("Value")
ende = time.time()
print('{:5.3f}s'.format(ende-start))
plt.show()
