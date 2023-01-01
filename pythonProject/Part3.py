from math import factorial
import numpy
import matplotlib.pyplot as mplib


# Monte Carlo simulation approach
def monte_carlo(ao):  # ao is the offered traffic for the simulation
    monteCarloGos = []  # list for Grade of Service values for Monte Carlo simulation

    for i in ao:  # for every integer value in ao, e.g ao = 10: 0,1,2,..,9

        lines = 42  # fixed number if lines
        calls = []  # list to hold 42 calls on the "channels"
        durations = numpy.random.normal(180, 30, i).astype(int)

        callTimes = numpy.random.randint(0, 3601, i)  # call times in the hour
        callTimes.sort()

        call = 0
        dropped = 0
        connectedCalls = 0

        for j in range(1, 3601):  # one hour in seconds
            for c in calls:
                if c <= j:
                    calls.pop(calls.index(c))

            if call < i and j in callTimes:
                if len(calls) < lines:
                    calls.append(durations[call] + j)
                    connectedCalls += 1
                    call += 1
                else:
                    dropped += 1
                    call += 1

        gos = (call - connectedCalls) / call  # calculate Grade of Service
        monteCarloGos.append(gos)  # add calculated GoS to list to return at end of method
        print('################## Calls Connected/ Dropped ##################')
        print('Total Calls: ' + str(call))
        print('Connected Calls: ' + str(connectedCalls))
        print('Dropped Calls: ' + str(dropped))
        print('####################################')

    return monteCarloGos


def erlang(n, ao):
    numerator = (ao ** n) / (factorial(n))
    denominator = 0
    for b in range(n + 1):
        denominator += (ao ** b) / factorial(b)
    gos = numerator / denominator
    return gos


erlang_Gos = []
monteCarlo_Gos = []

callsph = range(500, 10001, 500)
traffic = []

for i in callsph:
    t = round((i / 3600) * 180)
    traffic.append(t)
    erlang_Gos.append(erlang(42, t))  # erlang b formula

# run monte carlo simulation 5 times for each distribution type
for i in range(1, 6):
    monteCarlo_Gos.append(monte_carlo(callsph))

# get mean value of simulation runs
monteCarlo_Gos_mean = numpy.mean(monteCarlo_Gos, axis=0)
print("################## Monte Carlo GoS Mean ##################")
print(monteCarlo_Gos_mean)

# get standard deviation value of simulation runs
monteCarlo_Gos_std = numpy.std(monteCarlo_Gos, axis=0)
print("################## Monte Carlo GoS Standard Deviation ##################")
print(monteCarlo_Gos_std)

print("################## traffic ##################")
print(traffic)

print("################## Erlang GoS ##################")
print(erlang_Gos)

# Plots
mplib.plot(traffic, erlang_Gos, label='Erlang (Part 1)')
mplib.plot(traffic, monteCarlo_Gos_mean, label='Monte Carlo (Part 2)')
mplib.legend()
mplib.title("Comparison of Results from Part 1 & Part 2")
mplib.xlabel("Traffic")
mplib.ylabel("Grade of Service")
mplib.show()
