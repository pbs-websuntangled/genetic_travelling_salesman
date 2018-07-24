import matplotlib.pyplot as plt
import numpy as np
import time
from utils import calculate_rout_distance


class Route:

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
    number_of_cities = 3
    shape = (number_of_cities, 2)

    cities = np.random.choice(grid_size, shape)

    # create the routes
    number_of_routes = 20
    routes = []
    for _ in range(number_of_routes):

        route = np.random.choice(
            number_of_cities, number_of_cities, replace=False)
        routes.append(route)

    # calculate the distance and cost
    distances = []
    for route in routes:
        distance = calculate_rout_distance(route, cities, debug=debug)

        # add to distances
        distances.append(distance)
    distances = np.asarray(distances)

    # timer because it's a long process!!
    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    # and out of here

    #plt.plot(zip(*[cities[tour[i % 15]] for i in range(16) ])[0], zip(*[cities[tour[i % 15]] for i in range(16) ])[1], 'xb-', );
    # plt.show()

    plt.scatter(cities[:, 0], cities[:, 1])
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
