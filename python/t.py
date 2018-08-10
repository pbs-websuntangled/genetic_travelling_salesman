import matplotlib.pyplot as plt
import numpy as np
import sys
import cv2
from colours import get_colour
from return_provenance import return_provenance
import time
import os


provenance = ["route_pool_0 number 883", "Survivor", "Child", "Survivor", "Mutation", "Survivor", "Child Mother Reversed", "Survivor", "Child", "Survivor", "Child", "Survivor", "Child", "Survivor", "Mutation", "Survivor", "Child", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child", "Survivor", "Child", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child", "Survivor", "Child", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child", "Survivor", "Child", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Child", "Survivor", "Child", "Survivor",
              "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Leaked from route_pool_0",  "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Child Mother Reversed", "Survivor", "Survivor", "Survivor", "Child Father Reversed", "Survivor", "Survivor", "Survivor", "Survivor", "Survivor"]

provenance = return_provenance()

legend = {}

legend["Survivor"] = {}
legend["Survivor"]["colour"] = get_colour("light grey")

legend["Child"] = {}
legend["Child"]["colour"] = get_colour("lime green")

legend["Child Mother Reversed"] = {}
legend["Child Mother Reversed"]["colour"] = get_colour("green")

legend["Child Father Reversed"] = {}
legend["Child Father Reversed"]["colour"] = get_colour("green")

legend["Leaked from"] = {}
legend["Leaked from"]["colour"] = get_colour("orange")

legend["Mutation"] = {}
legend["Mutation"]["colour"] = get_colour("violet")


# start a new figure
plt.figure()

not_found = "not found =============================="
provenance_visualisation_stripe_width = 3
provenance_visualisation_stripe_white_space_width = 0
provenance_visualisation_width = provenance_visualisation_stripe_white_space_width + (len(
    provenance) - 1) * (provenance_visualisation_stripe_width + provenance_visualisation_stripe_white_space_width)
provenance_visualisation_height = int(provenance_visualisation_width * 0.1)
channels = 3
provenance_visualisation = np.zeros((
    provenance_visualisation_height, provenance_visualisation_width, channels), dtype=np.uint8) + 255

for iteraration_index, event in enumerate(provenance[1:]):

    match = legend.get(
        event, not_found)

    if match == not_found:
        match = legend.get(event[:len("Leaked from")], not_found)

    starts_at = iteraration_index * (provenance_visualisation_stripe_width +
                                     provenance_visualisation_stripe_white_space_width) + provenance_visualisation_stripe_white_space_width
    provenance_visualisation[:, starts_at:starts_at +
                             provenance_visualisation_stripe_width] = match["colour"]["bgr"]

    print(event, match)

# create a filename
start_time_formatted = time.strftime("%Y%m%d-%H%M%S")
filename_to_use = "ancestry" +\
    "__ts_" + str(start_time_formatted) +\
    ".png"
filename_to_use = os.path.join("outputNoGit", filename_to_use)

cv2.imwrite(filename_to_use, provenance_visualisation)


# start a new figure
plt.figure()

t = 1/0
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
