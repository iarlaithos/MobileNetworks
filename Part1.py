import math
import matplotlib.pyplot as mplib
import numpy as np


def erlang(n, calls, callDuration):

    ao = (calls/60) * callDuration
    numerator = (ao ** n) / (math.factorial(n))
    denominator = 0
    for b in range(n + 1):
        denominator += (ao ** b) / math.factorial(b)
    gos = numerator/denominator
    return gos


gosResults = []
t = 0
while True:

    gosResults.append(erlang(t, 600, 3))
    if gosResults[t] <= 0.01:
        break
    t+= 1


for x in gosResults:
    print('No. of channels: ' + str(gosResults.index(x)) )
    print(str(round((x*100),4)) + '%')


xAxis = np.linspace(0, len(gosResults), 1)
mplib.plot(gosResults, label='Erlang B')
mplib.xlabel('Number of Channels')
mplib.ylabel('Grade of Service')

mplib.title("Plot of Grade of Service vs the Number of Channels Available")

mplib.legend()
mplib.show()
