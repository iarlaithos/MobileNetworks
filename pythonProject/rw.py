import erlang as erl
from scipy.stats import erlang, expon
import numpy
import matplotlib.pyplot as plt

# Monte Carlo simulation
def monte_carlo(dist, traffic): # dist is distribution type, traffic is the offered traffic for the simulation

    mc_gos = []  # empty list to hold Grad of Service values for simulation

    for i in traffic:

        num_lines = 56  # fixed
        calls = []  # list to hold 56 calls on the "channels"

        # choosing distribution for call durations (normal, erlang, exponential) mean 2 minutes, spread 30 seconds
        if dist == 1:
            durations = numpy.random.normal(120, 30, i).astype(int)
        elif dist == 2:
            durations = expon.rvs(120, 30, i).astype(int)
        elif dist == 3:
            durations = erlang.rvs(a=4, loc=120, scale=30, size=i).astype(int)

        call_times = numpy.random.randint(0, 3601, i)  # call times in the hour
        call_times.sort()

        # set variables to 0 at beginning of loop
        call = 0
        calls_dropped = 0
        call_success = 0

        for j in range(1, 3601):  # one hour in seconds
            for c in calls:
                if c <= j:
                    calls.pop(calls.index(c))

            if call < i and j in call_times:
                if len(calls) < num_lines:
                    calls.append(durations[call] + j)
                    call_success += 1
                    call += 1
                else:
                    calls_dropped += 1
                    call += 1

        gos = (call - call_success)/call  # calculate Grade of Service
        mc_gos.append(gos)  # add calculated GoS to list to return at end of method

    return mc_gos
# end of method


erl_gos = []
mc_normal_gos = []
mc_exp_gos = []
mc_erlang_gos = []

calls_per_hour = range(500, 10001, 500)
traffic = []


for i in calls_per_hour:
    t = round((i / 3600) * 120)
    traffic.append(t)
    erl_gos.append(erl.b(t, 56))  # erlang b formula


# run monte carlo simulation 5 times for each distribution type
for i in range(1, 6):
    mc_normal_gos.append(monte_carlo(1, calls_per_hour))

    mc_exp_gos.append(monte_carlo(2, calls_per_hour))

    mc_erlang_gos.append(monte_carlo(3, calls_per_hour))


# get mean value of each distributions simulation runs
mc_erlang_mean = numpy.mean(mc_erlang_gos, axis=0)
mc_exp_mean = numpy.mean(mc_exp_gos, axis=0)
mc_normal_mean = numpy.mean(mc_normal_gos, axis=0)

print(mc_erlang_mean)
print(mc_exp_mean)
print(mc_normal_mean)

# get standard deviation value of each distributions simulation runs
print(numpy.std(mc_erlang_gos, axis=0))
print(numpy.std(mc_exp_gos, axis=0))
print(numpy.std(mc_normal_gos, axis=0))

# plot gos on graph
plt.plot(traffic, erl_gos, label='Erlang')
plt.plot(traffic, mc_erlang_mean, label='Monte Carlo Erlang')
plt.plot(traffic, mc_exp_mean, label='Monte Carlo Exponential')
plt.plot(traffic, mc_normal_mean, label='Monte Carlo Normal')
plt.legend()
plt.xlabel("Traffic")
plt.ylabel("Grade of Service")

plt.show()