from math import factorial, ceil
import numpy
import matplotlib.pyplot as mplib
import numpy as numpy


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

def erlang(n, callsph):
    erlangGos = []
    for i in callsph:
        ao = ceil((i / 3600) * 180)
        numerator = (ao ** n) / (factorial(n))
        denominator = 0
        for b in range(n + 1):
            denominator += (ao ** b) / factorial(b)
        gos = numerator / denominator
        erlangGos.append(gos)
    return erlangGos

erlang_gos = []
monteCarlo_Gos = []
total_traffic = []
# Call Proportions means the percentage of total traffic in a day during that hour
callProportions = [0.0009, 0.0005, 0.0004, 0.0004, 0.0008, 0.0044, 0.0168, 0.051, 0.0813, 0.0794, 0.0743, 0.0795,
                       0.0881, 0.089, 0.0866, 0.0848, 0.0821, 0.068, 0.047, 0.0306, 0.0183, 0.0095, 0.0043, 0.002]
# run monte carlo simulation 5 times for each distribution type
for i in range(0, 24):
    callspd = range(500, 10001, 500)
    callsph = [ceil(callProportions[i]*z) for z in callspd]
    traffic = []
    for j in callsph:
        t = ceil((j / 3600) * 180)
        traffic.append(t)
    total_traffic.append(traffic)

    erlang_gos.append(erlang(42, callsph))
    monteCarlo_Gos.append(monte_carlo(callsph))

traffic_mean = []
for x in range(0,20):
    sum = 0
    for y in total_traffic:
        sum += y[x]
    traffic_mean.append(sum/len(total_traffic))

# get erlang mean value of simulation runs
erlang_gos_mean = numpy.mean(erlang_gos, axis=0)
print("################## Erlang GoS Mean ##################")
print(erlang_gos_mean)

# get monte carlo mean value of simulation runs
monteCarlo_Gos_mean = numpy.mean(monteCarlo_Gos, axis=0)
print("################## Monte Carlo GoS Mean ##################")
print(monteCarlo_Gos_mean)

# get standard deviation value of simulation runs
monteCarlo_Gos_std = numpy.std(monteCarlo_Gos, axis=0)
print("################## Monte Carlo GoS Standard Deviation ##################")
print(monteCarlo_Gos_std)

# Plot
mplib.plot(traffic_mean, erlang_gos_mean, label='Erlang')
mplib.plot(traffic_mean, monteCarlo_Gos_mean, label='Monte Carlo')
mplib.legend()
mplib.title("Plot of Grade of Service vs Offered Traffic")
mplib.xlabel("Traffic")
mplib.ylabel("Grade of Service")
mplib.show()
