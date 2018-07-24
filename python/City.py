import matplotlib.pyplot as plt
import numpy as np
import time
from utils import calculate_rout_distance


class City:

    def __init__(self, x, y):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "__init__City"
        print("Starting", function_name)

        self.x = x
        self.y = y

        # save a name
        self.name = "City: " + str(x) + ", " + str(y)

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)


def run_tests(debug=False):

    # start a timer because it's a long process!!
    start_time, function_name = time.time(), "run_tests"
    print("Starting", function_name)

    # set the return code
    return_code = 0

    # create a city
    # city1 = City(3, 4)

    # low = 1
    # high = 10
    # size = (4, 2)
    #x = np.random.randint(low, high=high)

    # create the cities
    grid_size = 10
    low = 0
    number_of_cities = 3
    shape = (number_of_cities, 2)

    # generate some random cities
    cities = []

    for _ in range(number_of_cities):

        x = np.random.randint(low, high=grid_size, size=None, dtype='l')
        y = np.random.randint(low, high=grid_size, size=None, dtype='l')

        cities.append(City(x, y))

    # timer because it's a long process!!
    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    # and out of here

    # get data for plotting
    x = []
    y = []
    for city in cities:
        x.append(city.x)
        y.append(city.y)

    plt.scatter(x, y)
    plt.show()

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
