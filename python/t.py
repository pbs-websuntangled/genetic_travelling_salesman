import matplotlib.pyplot as plt
import numpy as np
import sys
import cv2
from colours import get_colour
from return_provenance import return_provenance
import time
import os


def visualise_provenance(provenance, name):

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

    # create a blank legend image

    legend_visualisation_line_space = 100
    legend_visualisation_line_thickness = int(
        legend_visualisation_line_space / 10)
    legend_visualisation_height = (
        len(legend) + 1) * legend_visualisation_line_space
    golden_ratio = 1.61803398875

    legend_visualisation_width = int(
        legend_visualisation_height * golden_ratio)
    legend_visualisation = np.zeros(
        (legend_visualisation_height, legend_visualisation_width, 3)) + 255
    legend_visualisation_line_length = legend_visualisation_line_space * 3
    text_font = cv2.FONT_HERSHEY_DUPLEX

    text_colour = (0, 0, 0)

    # loop through each of the legend entries and draw the line with description
    for entry_index, entry in enumerate(legend):

        colour = legend[entry]["colour"]["bgr"]
        point_1 = (legend_visualisation_line_space, (entry_index + 1)
                   * legend_visualisation_line_space)
        point_2 = (legend_visualisation_line_length, (entry_index + 1)
                   * legend_visualisation_line_space)

        text_point = point_2[0] + legend_visualisation_line_space, point_2[1]
        cv2.line(legend_visualisation, point_1, point_2, colour,
                 thickness=legend_visualisation_line_thickness)

        cv2.putText(legend_visualisation, entry,
                    text_point, text_font, 1, text_colour)

        print("entry", entry)

        print(legend[entry])

    # create a filename
    start_time_formatted = time.strftime("%Y%m%d-%H%M%S")
    filename_to_use = "legend" +\
        "__ts_" + str(start_time_formatted) +\
        ".png"
    filename_to_use = os.path.join("outputNoGit", filename_to_use)

    cv2.imwrite(filename_to_use, legend_visualisation)

    not_found = "not found =============================="
    provenance_visualisation_stripe_width = 3
    provenance_visualisation_stripe_white_space_width = 0
    provenance_visualisation_width = provenance_visualisation_stripe_white_space_width + (len(
        provenance) - 1) * (provenance_visualisation_stripe_width + provenance_visualisation_stripe_white_space_width)
    provenance_visualisation_height = int(provenance_visualisation_width * 0.1)
    provenance_visualisation_title_height = legend_visualisation_line_space * 2
    channels = 3
    provenance_visualisation = np.zeros((
        provenance_visualisation_height + provenance_visualisation_title_height, provenance_visualisation_width, channels), dtype=np.uint8) + 255

    stripes_only = provenance_visualisation[provenance_visualisation_title_height:, :, :]

    # add the title to the white bar above the stripes
    text_point = (legend_visualisation_line_space,
                  int(1.2 * legend_visualisation_line_space))
    title_text_scale_factor = 3
    cv2.putText(provenance_visualisation, "Ancestry of shortest route: " + name,
                text_point, text_font, title_text_scale_factor, text_colour)

    # fill in the duplex spindly font
    # bit of a pain but it looks bad if you don't
    for channel_index in range(3):
        channel = provenance_visualisation[:, :, channel_index]
        channel[:] = cv2.erode(channel, None, iterations=1)

    # loop round all the evolutiuonary events and create the
    # vertical stripe in the image to reflect that
    for iteraration_index, event in enumerate(provenance[1:]):

        # find the correct entry in the legend table for this
        # evolution event
        match = legend.get(
            event, not_found)

        # if it wasn't there, then it must be one of the
        # ones containing some additional data
        if match == not_found:
            match = legend.get(event[:len("Leaked from")], not_found)

        starts_at = iteraration_index * (provenance_visualisation_stripe_width +
                                         provenance_visualisation_stripe_white_space_width) + provenance_visualisation_stripe_white_space_width
        stripes_only[:, starts_at:starts_at +
                     provenance_visualisation_stripe_width] = match["colour"]["bgr"]

    # create a filename
    start_time_formatted = time.strftime("%Y%m%d-%H%M%S")
    filename_to_use = "ancestry" +\
        "__ts_" + str(start_time_formatted) +\
        ".png"
    filename_to_use = os.path.join("outputNoGit", filename_to_use)

    cv2.imwrite(filename_to_use, provenance_visualisation)


name, provenance = return_provenance()

visualise_provenance(provenance, name)

t = 1/0
# ======================================================================================

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
