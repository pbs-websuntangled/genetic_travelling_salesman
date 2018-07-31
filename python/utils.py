import time
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
import scipy.ndimage


def plt_to_numpy_array(plt, debug=False):

    # start a timer because it's a long process!!
    start_time, function_name = time.time(), "plt_to_numpy_array"
    print("Starting", function_name)

    # set up the filename to save the histogram
    filenameToUse = "__random_" + str(int(np.random.rand() * 1000000000))

    plt.savefig(os.path.join('outputNoGit',
                             filenameToUse + "__deleteThis_y.png"))

    # read the temp image back in so I can add it to the inclusion image
    tempImage = cv2.imread(os.path.join(
        'outputNoGit', filenameToUse + "__deleteThis_y.png"))

    # and now clean up by deleting that file I just created
    os.remove(os.path.join('outputNoGit',
                           filenameToUse + "__deleteThis_y.png"))

    # timer because it's a long process!!
    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    return tempImage


def figure_to_numpy(figure):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param figure a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # comes from here:
    # http://www.icare.univ-lille1.fr/tutorials/convert_a_matplotlib_figure

    # draw the renderer
    figure.canvas.draw()

    # Get the RGBA buffer from the figure
    width, height = figure.canvas.get_width_height()
    figure_as_numpy_array = np.fromstring(
        figure.canvas.tostring_argb(), dtype=np.uint8)
    figure_as_numpy_array.shape = (width, height, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    figure_as_numpy_array = np.roll(figure_as_numpy_array, 3, axis=2)

    return figure_as_numpy_array


def calculate_rout_distance(route, cities, debug=False):

    # start a timer because it's a long process!!
    start_time, function_name = time.time(), "calculate_rout_distance"
    print("Starting", function_name)

    # go through and calculate the distance
    distance = 0
    first_time_through = True

    for city_index in route:

        # if it's the first city then move to the next
        if first_time_through:
            first_time_through = False
            continue

        # calculate the distance
        this_city = cities[city_index]
        previous_city = cities[city_index - 1]

        distance_step_x = this_city[0] - previous_city[0]
        distance_step_y = this_city[1] - previous_city[1]
        distance_step = (distance_step_x ** 2 +
                         distance_step_y ** 2) ** 0.5

        # accumulate the distance
        distance = distance + distance_step

    # I've done the route, so go back to the beginning
    this_city = cities[route[0]]
    previous_city = cities[route[-1]]

    distance_step_x = this_city[0] - previous_city[0]
    distance_step_y = this_city[1] - previous_city[1]
    distance_step = (distance_step_x ** 2 +
                     distance_step_y ** 2) ** 0.5

    # accumulate the distance
    distance = distance + distance_step

    # timer because it's a long process!!
    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    # and out of here
    return distance


def run_tests(debug=False):

    # start a timer because it's a long process!!
    start_time, function_name = time.time(), "run_tests"
    print("Starting", function_name)

    # set the return code
    return_code = 0

    # set up the cities
    cities = [[0, 0], [3, 4], [3, 0]]

    # set up the route
    route = [0, 1, 2]  # should be 12

    # calculate the jorney
    distance = calculate_rout_distance(route, cities, debug=False)

    # did the test work
    if 12 == distance:
        print("The distance test worked")

    else:
        print("The distance test did not work")

    plt.figure()
    plt.plot([1, 2, 3, 4])

    array = plt_to_numpy_array(plt)

    cv2.imwrite(os.path.join("outputNoGit", "test.png"), array)

    # timer because it's a long process!!
    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    # and out of here
    return return_code


if __name__ == '__main__':

    debug = True

    # just make sure that the random numbers generate
    # consistently for testing purposes
    np.random.seed(1)

    # do the run_tests
    return_code = run_tests(debug=debug)

    # final return code
    print("return_code", return_code)
