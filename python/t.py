import matplotlib.pyplot as plt
import numpy as np
import sys

test = sys.maxsize

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
