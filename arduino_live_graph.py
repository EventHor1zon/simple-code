#!/usr/bin/python

# program for updating a graph LIVE!!!
# interesting for sensor posibilities
# Learn!!!
#
#
# Small program to use MATPLOTLIB alongside arduino output
# to live-graph output from light dependent resistor
# /dev/ttyACM0 = arduino 
# BUGS: some bugs generating the graph due to arduino
# spewing noise at the beginning of a serial connection
# FIXES: parsing the results into expected values,
# 	using a button to begin the capture or serial out
# 	on arduino removes noise
# Looks nice, works reasonably well


import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style as style

style.use('fivethirtyeight')
serPort = "/dev/ttyACM0"
baud=9600

ser=serial.Serial(serPort, baud)
time.sleep(5)
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax1.clear()
xs=[]
ys=[]
def animate(i):
    graph_data=ser.readline()
    print graph_data
    if graph_data.find(":")==-1:
        return
    data=graph_data.split(":")
    if data[0] == None or data[1] == None:
        return
    data[1].strip("\r\n")
    xs.append(float(data[0]))
    ys.append(float(data[1]))
    ax1.plot(xs, ys)

plt.xlabel('Time')
plt.ylabel('Light level')

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
