import matplotlib.pyplot as plt
import numpy as np
import sys


provenance = ["route_pool_0 number 883", "Survivor", "Child", "Survivor", "Mutation", "Survivor", "Child Mother Reversed", "Survivor", "Child", "Survivor", "Child", "Survivor", "Child", "Survivor", "Mutation", "Survivor", "Child", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child", "Survivor", "Child", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child", "Survivor", "Child", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child", "Survivor", "Child", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Child", "Survivor", "Child", "Survivor",
              "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Leaked from route_pool_0",  "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor"]

legend = {}

legend["Survivor"] = {}
legend["Survivor"]["colour"] = "orange"

legend["Child"] = {}
legend["Child"]["colour"] = "green"

legend["Child Mother Reversed"] = {}
legend["Child Mother Reversed"]["colour"] = "red"

legend["Child Father Reversed"] = {}
legend["Child Father Reversed"]["colour"] = "pink"

legend["Leaked from"] = {}
legend["Leaked from"]["colour"] = "blue"

legend["Mutation"] = {}
legend["Mutation"]["colour"] = "black"

# start a new figure
plt.figure()

not_found = "not found =============================="

for iteraration_index, event in enumerate(provenance[1:]):

    match = legend.get(
        event, not_found)

    if match == not_found:
        match = legend.get(event[:len("Leaked from")], not_found)

    print(event, match)


# start a new figure
plt.figure()

# generate the set of random numbers in one hit
number_of_routes = 10000000

death_tokens0 = np.random.rand(number_of_routes)

death_tokens1 = 1 - \
    np.random.rand(number_of_routes) * np.random.rand(number_of_routes)

death_tokens2 = 1. - death_tokens0 * death_tokens0

count0, bins0, _ = plt.hist(death_tokens0, 100, normed=False)
count1, bins1, _ = plt.hist(death_tokens1, 100, normed=False)
count2, bins2, _ = plt.hist(death_tokens2, 100, normed=False)

# finish that one
plt.close('all')

# start a new figure
plt.figure()

plt.plot(count0, c="blue")
plt.plot(count1, c="red")
plt.plot(count2, c="green")
plt.show()

break_here = True
